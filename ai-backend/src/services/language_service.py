"""Language detection and routing service for multilingual support."""

from typing import Dict, Optional, Tuple
from enum import Enum

from langdetect import detect, LangDetectException
from src.models.requests import LocaleEnum


class CulturalContext(str, Enum):
    """Cultural context identifiers."""
    
    PORTUGUESE_BRAZIL = "pt_BR"
    PORTUGUESE_PORTUGAL = "pt_PT"
    ENGLISH_US = "en_US"
    ENGLISH_UK = "en_UK"


class LanguageDetectionService:
    """Service for detecting language and routing to appropriate agents."""
    
    def __init__(self):
        """Initialize language detection service."""
        self.supported_languages = {
            "en": LocaleEnum.EN,
            "pt": LocaleEnum.PT,
        }
        
        # Cultural context mappings
        self.cultural_contexts = {
            LocaleEnum.EN: {
                "default": CulturalContext.ENGLISH_US,
                "variants": [CulturalContext.ENGLISH_US, CulturalContext.ENGLISH_UK]
            },
            LocaleEnum.PT: {
                "default": CulturalContext.PORTUGUESE_BRAZIL,
                "variants": [CulturalContext.PORTUGUESE_BRAZIL, CulturalContext.PORTUGUESE_PORTUGAL]
            }
        }
    
    def detect_language(self, text: str, fallback: LocaleEnum = LocaleEnum.EN) -> LocaleEnum:
        """
        Detect language from user text input.
        
        Args:
            text: User input text
            fallback: Fallback locale if detection fails
            
        Returns:
            Detected locale enum
        """
        if not text or len(text.strip()) < 3:
            return fallback
        
        try:
            detected_lang = detect(text)
            
            # Map detected language to supported locale
            if detected_lang in self.supported_languages:
                return self.supported_languages[detected_lang]
            
            # Handle language variants (e.g., pt-BR, pt-PT both map to pt)
            lang_code = detected_lang.split("-")[0]
            if lang_code in self.supported_languages:
                return self.supported_languages[lang_code]
            
            return fallback
            
        except LangDetectException:
            return fallback
    
    def get_cultural_context(
        self, 
        locale: LocaleEnum, 
        user_preferences: Optional[Dict] = None
    ) -> CulturalContext:
        """
        Get cultural context for the given locale.
        
        Args:
            locale: User locale
            user_preferences: Optional user preferences for cultural variant
            
        Returns:
            Cultural context identifier
        """
        if locale not in self.cultural_contexts:
            return CulturalContext.ENGLISH_US
        
        context_info = self.cultural_contexts[locale]
        
        # Check if user has specific cultural preference
        if user_preferences and "cultural_variant" in user_preferences:
            preferred = user_preferences["cultural_variant"]
            if preferred in context_info["variants"]:
                return preferred
        
        return context_info["default"]
    
    def get_agent_routing_config(
        self, 
        locale: LocaleEnum, 
        cultural_context: CulturalContext
    ) -> Dict[str, str]:
        """
        Get agent routing configuration based on locale and cultural context.
        
        Args:
            locale: User locale
            cultural_context: Cultural context
            
        Returns:
            Dictionary with agent routing configuration
        """
        routing_config = {
            "locale": locale.value,
            "cultural_context": cultural_context.value,
            "language_model_instructions": self._get_language_instructions(locale),
            "cultural_adaptation_rules": self._get_cultural_rules(cultural_context),
            "example_style": self._get_example_style(cultural_context),
            "communication_style": self._get_communication_style(cultural_context)
        }
        
        return routing_config
    
    def _get_language_instructions(self, locale: LocaleEnum) -> str:
        """Get language-specific instructions for agents."""
        instructions = {
            LocaleEnum.EN: (
                "Respond in clear, natural English. Use appropriate terminology "
                "for cyber ethics and digital literacy. Maintain a supportive, "
                "educational tone."
            ),
            LocaleEnum.PT: (
                "Responda em português claro e natural. Use terminologia apropriada "
                "para ética cibernética e alfabetização digital. Mantenha um tom "
                "educativo e de apoio."
            )
        }
        return instructions.get(locale, instructions[LocaleEnum.EN])
    
    def _get_cultural_rules(self, cultural_context: CulturalContext) -> Dict[str, str]:
        """Get cultural adaptation rules for content generation."""
        rules = {
            CulturalContext.ENGLISH_US: {
                "formality": "moderate",
                "directness": "high",
                "examples": "US-centric (social media platforms, news sources)",
                "concerns": "privacy, data security, political polarization"
            },
            CulturalContext.ENGLISH_UK: {
                "formality": "moderate-high",
                "directness": "moderate",
                "examples": "UK-centric (BBC, UK social issues)",
                "concerns": "privacy, GDPR, online safety"
            },
            CulturalContext.PORTUGUESE_BRAZIL: {
                "formality": "moderate",
                "directness": "moderate",
                "examples": "Brazilian context (WhatsApp, local news, social issues)",
                "concerns": "fake news, political disinformation, WhatsApp chains"
            },
            CulturalContext.PORTUGUESE_PORTUGAL: {
                "formality": "high",
                "directness": "moderate",
                "examples": "Portuguese context (European news, GDPR)",
                "concerns": "privacy, data protection, European regulations"
            }
        }
        return rules.get(cultural_context, rules[CulturalContext.ENGLISH_US])
    
    def _get_example_style(self, cultural_context: CulturalContext) -> str:
        """Get example style for the cultural context."""
        styles = {
            CulturalContext.ENGLISH_US: (
                "Use examples from US social media (Facebook, Twitter/X, Instagram), "
                "US news sources, and American cultural references."
            ),
            CulturalContext.ENGLISH_UK: (
                "Use examples from UK social media, BBC, UK news sources, "
                "and British cultural references."
            ),
            CulturalContext.PORTUGUESE_BRAZIL: (
                "Use exemplos do contexto brasileiro (WhatsApp, redes sociais brasileiras, "
                "notícias locais). Referências culturais brasileiras são apropriadas."
            ),
            CulturalContext.PORTUGUESE_PORTUGAL: (
                "Use exemplos do contexto português (redes sociais europeias, "
                "notícias portuguesas). Referências culturais portuguesas são apropriadas."
            )
        }
        return styles.get(cultural_context, styles[CulturalContext.ENGLISH_US])
    
    def _get_communication_style(self, cultural_context: CulturalContext) -> str:
        """Get communication style for the cultural context."""
        styles = {
            CulturalContext.ENGLISH_US: (
                "Direct, friendly, and encouraging. Use casual but professional language."
            ),
            CulturalContext.ENGLISH_UK: (
                "Polite, clear, and supportive. Slightly more formal than US English."
            ),
            CulturalContext.PORTUGUESE_BRAZIL: (
                "Amigável, acolhedor e encorajador. Use linguagem acessível e próxima."
            ),
            CulturalContext.PORTUGUESE_PORTUGAL: (
                "Educado, claro e profissional. Mantenha um tom respeitoso e formal."
            )
        }
        return styles.get(cultural_context, styles[CulturalContext.ENGLISH_US])
    
    def adapt_agent_prompt(
        self, 
        base_prompt: str, 
        locale: LocaleEnum, 
        cultural_context: CulturalContext
    ) -> str:
        """
        Adapt agent prompt for specific locale and cultural context.
        
        Args:
            base_prompt: Base agent prompt
            locale: Target locale
            cultural_context: Cultural context
            
        Returns:
            Adapted prompt with cultural and linguistic instructions
        """
        routing_config = self.get_agent_routing_config(locale, cultural_context)
        
        adapted_prompt = f"""{base_prompt}

LANGUAGE AND CULTURAL ADAPTATION:
- Language: {routing_config['locale']}
- Cultural Context: {routing_config['cultural_context']}
- Instructions: {routing_config['language_model_instructions']}
- Communication Style: {routing_config['communication_style']}
- Example Style: {routing_config['example_style']}

CULTURAL RULES:
{self._format_cultural_rules(routing_config['cultural_adaptation_rules'])}

Always maintain these language and cultural adaptations in your responses.
"""
        return adapted_prompt
    
    def _format_cultural_rules(self, rules: Dict[str, str]) -> str:
        """Format cultural rules for prompt inclusion."""
        formatted = []
        for key, value in rules.items():
            formatted.append(f"- {key.capitalize()}: {value}")
        return "\n".join(formatted)
    
    def validate_locale(self, locale: str) -> Tuple[bool, Optional[LocaleEnum]]:
        """
        Validate if locale is supported.
        
        Args:
            locale: Locale string to validate
            
        Returns:
            Tuple of (is_valid, locale_enum)
        """
        try:
            locale_enum = LocaleEnum(locale.lower())
            return True, locale_enum
        except ValueError:
            return False, None
    
    def get_supported_locales(self) -> Dict[str, str]:
        """
        Get list of supported locales with descriptions.
        
        Returns:
            Dictionary mapping locale codes to descriptions
        """
        return {
            "en": "English (US/UK)",
            "pt": "Português (Brasil/Portugal)"
        }


# Singleton instance
_language_service: Optional[LanguageDetectionService] = None


def get_language_service() -> LanguageDetectionService:
    """Get singleton instance of language detection service."""
    global _language_service
    if _language_service is None:
        _language_service = LanguageDetectionService()
    return _language_service
