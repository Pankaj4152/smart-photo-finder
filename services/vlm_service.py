from pathlib import Path
from typing import Optional, List, Tuple, Dict
import io

from nexaai import VLM
from nexaai.common import (
    GenerationConfig,
    ModelConfig,
    MultiModalMessage,
    MultiModalMessageContent
)

from logger import get_logger
from config import config


logger = get_logger(__name__)

class VLMService:
    def __init__(self):
        logger.debug("Initializing VLMService...")
        self.model: Optional[VLM] = None
        self._load_model()
        logger.debug("VLMService initialized.")

    def _load_model(self):
        logger.info("Loading VLM model...")
        
        try:
            m_cfg = ModelConfig(
                n_gpu_layers=config.gpu_layers,
                n_ctx=config.vlm_n_ctx,
                n_threads=config.vlm_n_threads,
                n_threads_batch=config.vlm_n_threads_batch,
                n_batch=config.vlm_n_batch,
                n_ubatch=config.vlm_n_ubatch
            )
            logger.info(f"ModelConfig: {m_cfg}")

            logger.debug(f"Paths -> Model: {config.vlm_model_path}, mmproj: {config.mmproj_path}")
            
            self.vlm = VLM.from_(
                name_or_path=config.vlm_model_path,
                mmproj_path=config.mmproj_path,
                m_cfg = m_cfg,
                plugin_id = config.plugin_id
            )
            logger.debug("VLM loaded successfully.")

        except Exception as e:
            logger.error(f"Model load failed: {e}")
            logger.debug("Full traceback:", exc_info=True)
            raise RuntimeError(f"VLM model loading failed. {e}")
        

    # State Reset
    def _reset_state(self):
        """
        Ensures the model has no leftover state between calls
        (important for consistent descriptions)
        """
        try:
            if hasattr(self.vlm, "reset"):
                self.vlm.reset()

            if hasattr(self.vlm, "_model"):
                inner = self.vlm._model
                if hasattr(inner, "reset_cache"):
                    inner.reset_cache()

            logger.debug("VLM model state reset.")
        except Exception as e:
            logger.warning(f"State reset failed, continuing anyway: {e}")

    def _validate_image_paths(self, image_paths: List[str]) -> Tuple[List[str], List[str]]:
        """
        Validate image paths and separate valid/invalid ones.
        
        Args:
            image_paths: List of image paths to validate
            
        Returns:
            Tuple of (valid_paths, invalid_paths)
        """
        valid_paths = []
        invalid_paths = []
        
        for path in image_paths:
            if Path(path).exists():
                valid_paths.append(path)
            else:
                invalid_paths.append(path)
                logger.warning(f"Image missing: {path}")
        
        return valid_paths, invalid_paths

    def generate_description(self, image_path: str) -> Optional[str]:
        if not self.vlm:
            logger.error("VLM not initialized.")
            return None

        if not Path(image_path).exists():
            logger.warning(f"Image missing: {image_path}")
            return None
        
        logger.info(f"Processing image: {image_path}")
        logger.debug("Resetting VLM state...")
        self._reset_state()

        prompt = (
            "Describe this image in detail. Include:"
            " objects, people, background, colors, actions,"
            " and overall context. Be descriptive and precise."
        )

        # Build Conversation
        conversation = [
            MultiModalMessage(
                role="user",
                content=[
                    MultiModalMessageContent(type="text", text=prompt),
                    MultiModalMessageContent(type="image", path=image_path),
                ],
            )
        ]

        try:
            # Format prompt
            formatted_prompt = self.vlm.apply_chat_template(conversation)

            # Streaming generation
            buffer = io.StringIO()
            logger.debug(f"Generating tokens for: {image_path}")


            for token in self.vlm.generate_stream(
                formatted_prompt,
                g_cfg=GenerationConfig(
                    max_tokens=config.max_tokens,
                    image_paths=[image_path]
                )
            ):
                buffer.write(token)

            description = buffer.getvalue().strip()

            if not description:
                logger.warning(f"No description generated: {image_path}")
                return None

            logger.info(f"Description generated: {image_path}")
            logger.debug(f"Output length: {len(description)} chars")

            return description

        except Exception as e:
            logger.error(f"Generation failed for {image_path}: {e}")
            logger.debug("Traceback:", exc_info=True)
            return None
        
    def generate_descriptions_batch(self, image_paths: List[str]) -> Dict[str, Optional[str]]:
        """
        Generate descriptions for a batch of images.
        
        Args:
            image_paths: List of image paths
        Returns:
            Dict mapping image paths to descriptions (or None on failure)
        """

        if not self.vlm:
            logger.error("VLM not initialized.")
            return {path: None for path in image_paths}
        
        if not image_paths:
            logger.warning("No image paths provided for batch description generation.")
            return {}

        # Validate paths
        valid_paths, invalid_paths = self._validate_image_paths(image_paths)

        # Initialize results with None for invalid paths
        results = {path: None for path in invalid_paths}

        if not valid_paths:
            logger.warning("No valid image paths found.")
            return results
        
        logger.info(f"Batch processing {len(valid_paths)} valid images...")

        # Reset state once for the entire batch
        logger.debug("Resetting VLM state for batch processing...")
        self._reset_state()

        # Common prompt for all images
        prompt = (
            "Describe this image in detail. Include:"
            " objects, people, background, colors, actions,"
            " and overall context. Be descriptive and precise."
        )
