"""Culturally-aware content generation service."""

from typing import Dict, List, Optional
from enum import Enum

from src.models.requests import LocaleEnum, DisinformationType
from src.services.language_service import CulturalContext


class ContentCategory(str, Enum):
    """Content categories for cultural adaptation."""
    
    EXAMPLES = "examples"
    SCENARIOS = "scenarios"
    DISINFORMATION_PATTERNS = "disinformation_patterns"
    SOCIAL_MEDIA_POSTS = "social_media_posts"
    COMMUNICATION_STYLES = "communication_styles"


class CulturalContentService:
    """Service for generating culturally-aware educational content."""
    
    def __init__(self):
        """Initialize cultural content service."""
        self._initialize_content_templates()
    
    def _initialize_content_templates(self):
        """Initialize content templates for different cultures."""
        self.content_templates = {
            CulturalContext.ENGLISH_US: self._get_us_content_templates(),
            CulturalContext.ENGLISH_UK: self._get_uk_content_templates(),
            CulturalContext.PORTUGUESE_BRAZIL: self._get_brazil_content_templates(),
            CulturalContext.PORTUGUESE_PORTUGAL: self._get_portugal_content_templates(),
        }
    
    def get_cultural_examples(
        self, 
        cultural_context: CulturalContext,
        topic: str,
        count: int = 3
    ) -> List[str]:
        """
        Get culturally-appropriate examples for a topic.
        
        Args:
            cultural_context: Cultural context
            topic: Topic for examples
            count: Number of examples to return
            
        Returns:
            List of culturally-appropriate examples
        """
        templates = self.content_templates.get(cultural_context, {})
        examples = templates.get(ContentCategory.EXAMPLES, {}).get(topic, [])
        return examples[:count]
    
    def get_disinformation_patterns(
        self,
        cultural_context: CulturalContext,
        disinformation_type: DisinformationType
    ) -> Dict[str, any]:
        """
        Get culturally-specific disinformation patterns.
        
        Args:
            cultural_context: Cultural context
            disinformation_type: Type of disinformation
            
        Returns:
            Dictionary with disinformation patterns and concerns
        """
        templates = self.content_templates.get(cultural_context, {})
        patterns = templates.get(ContentCategory.DISINFORMATION_PATTERNS, {})
        return patterns.get(disinformation_type.value, {})
    
    def generate_social_media_scenario(
        self,
        cultural_context: CulturalContext,
        scenario_type: str,
        difficulty: int = 1
    ) -> Dict[str, any]:
        """
        Generate culturally-appropriate social media scenario.
        
        Args:
            cultural_context: Cultural context
            scenario_type: Type of scenario
            difficulty: Difficulty level (1-5)
            
        Returns:
            Dictionary with scenario details
        """
        templates = self.content_templates.get(cultural_context, {})
        scenarios = templates.get(ContentCategory.SCENARIOS, {}).get(scenario_type, [])
        
        if not scenarios:
            return self._get_default_scenario(cultural_context)
        
        # Filter by difficulty if available
        filtered = [s for s in scenarios if s.get("difficulty", 1) == difficulty]
        if not filtered:
            filtered = scenarios
        
        return filtered[0] if filtered else scenarios[0]

    def get_communication_style_guide(
        self,
        cultural_context: CulturalContext
    ) -> Dict[str, str]:
        """
        Get communication style guide for cultural context.
        
        Args:
            cultural_context: Cultural context
            
        Returns:
            Dictionary with communication style guidelines
        """
        templates = self.content_templates.get(cultural_context, {})
        return templates.get(ContentCategory.COMMUNICATION_STYLES, {})
    
    def _get_us_content_templates(self) -> Dict:
        """Get content templates for US English context."""
        return {
            ContentCategory.EXAMPLES: {
                "privacy": [
                    "Facebook data sharing with third-party apps",
                    "Google tracking your location history",
                    "TikTok collecting user data"
                ],
                "deepfakes": [
                    "Fake celebrity endorsement videos on Instagram",
                    "Political deepfakes during election season",
                    "AI-generated news anchor videos"
                ],
                "social_media": [
                    "Twitter/X misinformation during breaking news",
                    "Facebook groups spreading conspiracy theories",
                    "Instagram influencer scams"
                ]
            },
            ContentCategory.DISINFORMATION_PATTERNS: {
                "health": {
                    "common_topics": ["vaccine misinformation", "miracle cures", "FDA conspiracies"],
                    "platforms": ["Facebook", "YouTube", "Twitter/X"],
                    "red_flags": ["Unverified medical claims", "Anti-government rhetoric", "Emotional manipulation"]
                },
                "politics": {
                    "common_topics": ["election fraud", "deep state", "partisan propaganda"],
                    "platforms": ["Twitter/X", "Facebook", "Reddit"],
                    "red_flags": ["Extreme partisan language", "Unverified sources", "Emotional appeals"]
                }
            },
            ContentCategory.SCENARIOS: {
                "catfish": [
                    {
                        "difficulty": 1,
                        "description": "Teen pretending to be older on Instagram",
                        "red_flags": ["Inconsistent age claims", "Avoids video calls", "Asks for money"],
                        "platform": "Instagram"
                    }
                ],
                "fake_news": [
                    {
                        "difficulty": 1,
                        "description": "Viral tweet with misleading statistics",
                        "red_flags": ["No source cited", "Emotional language", "Suspicious account"],
                        "platform": "Twitter/X"
                    }
                ]
            },
            ContentCategory.COMMUNICATION_STYLES: {
                "tone": "friendly and direct",
                "formality": "casual-professional",
                "examples_style": "Use US social media platforms and news sources",
                "cultural_references": "American pop culture, US news events"
            }
        }
    
    def _get_uk_content_templates(self) -> Dict:
        """Get content templates for UK English context."""
        return {
            ContentCategory.EXAMPLES: {
                "privacy": [
                    "GDPR violations by tech companies",
                    "NHS data sharing concerns",
                    "UK government surveillance programmes"
                ],
                "deepfakes": [
                    "Fake BBC news reports",
                    "Manipulated videos of UK politicians",
                    "AI-generated royal family content"
                ],
                "social_media": [
                    "WhatsApp misinformation in UK communities",
                    "Facebook groups spreading Brexit misinformation",
                    "Twitter scams targeting UK users"
                ]
            },
            ContentCategory.DISINFORMATION_PATTERNS: {
                "health": {
                    "common_topics": ["NHS misinformation", "vaccine hesitancy", "alternative medicine"],
                    "platforms": ["Facebook", "WhatsApp", "Twitter"],
                    "red_flags": ["Anti-NHS rhetoric", "Unverified health claims", "Conspiracy theories"]
                },
                "politics": {
                    "common_topics": ["Brexit misinformation", "parliamentary scandals", "immigration"],
                    "platforms": ["Twitter", "Facebook", "WhatsApp"],
                    "red_flags": ["Extreme political views", "Unverified claims", "Divisive language"]
                }
            },
            ContentCategory.SCENARIOS: {
                "catfish": [
                    {
                        "difficulty": 1,
                        "description": "Person pretending to be from London on dating app",
                        "red_flags": ["Inconsistent location", "Avoids meeting", "Asks for money"],
                        "platform": "Dating apps"
                    }
                ]
            },
            ContentCategory.COMMUNICATION_STYLES: {
                "tone": "polite and clear",
                "formality": "moderate-formal",
                "examples_style": "Use UK platforms, BBC, and British news sources",
                "cultural_references": "British culture, UK current events"
            }
        }
    
    def _get_brazil_content_templates(self) -> Dict:
        """Get content templates for Brazilian Portuguese context."""
        return {
            ContentCategory.EXAMPLES: {
                "privacy": [
                    "Vazamento de dados pessoais no Brasil",
                    "Compartilhamento de dados pelo WhatsApp",
                    "Rastreamento de localização por aplicativos"
                ],
                "deepfakes": [
                    "Vídeos falsos de políticos brasileiros",
                    "Deepfakes de celebridades brasileiras",
                    "Notícias falsas com vídeos manipulados"
                ],
                "social_media": [
                    "Correntes de WhatsApp com fake news",
                    "Grupos de Facebook espalhando desinformação",
                    "Golpes no Instagram e TikTok"
                ]
            },
            ContentCategory.DISINFORMATION_PATTERNS: {
                "health": {
                    "common_topics": ["desinformação sobre vacinas", "curas milagrosas", "teorias da conspiração sobre saúde"],
                    "platforms": ["WhatsApp", "Facebook", "Instagram"],
                    "red_flags": ["Correntes de WhatsApp", "Fontes não verificadas", "Apelo emocional forte"]
                },
                "politics": {
                    "common_topics": ["fake news política", "manipulação eleitoral", "teorias conspiratórias"],
                    "platforms": ["WhatsApp", "Facebook", "Twitter/X"],
                    "red_flags": ["Linguagem extremista", "Fontes duvidosas", "Manipulação emocional"]
                },
                "fake_news": {
                    "common_topics": ["notícias falsas virais", "boatos", "desinformação em massa"],
                    "platforms": ["WhatsApp", "Facebook", "Instagram"],
                    "red_flags": ["Correntes virais", "Sem fonte confiável", "Urgência artificial"]
                }
            },
            ContentCategory.SCENARIOS: {
                "catfish": [
                    {
                        "difficulty": 1,
                        "description": "Pessoa fingindo ser de outra cidade no WhatsApp",
                        "red_flags": ["Evita chamadas de vídeo", "Pede dinheiro", "História inconsistente"],
                        "platform": "WhatsApp"
                    }
                ],
                "fake_news": [
                    {
                        "difficulty": 1,
                        "description": "Corrente de WhatsApp com notícia falsa",
                        "red_flags": ["Sem fonte", "Linguagem alarmista", "Pede compartilhamento"],
                        "platform": "WhatsApp"
                    },
                    {
                        "difficulty": 2,
                        "description": "Post viral no Facebook com informação manipulada",
                        "red_flags": ["Fonte desconhecida", "Imagem editada", "Contexto removido"],
                        "platform": "Facebook"
                    }
                ]
            },
            ContentCategory.COMMUNICATION_STYLES: {
                "tone": "amigável e acolhedor",
                "formality": "informal-moderado",
                "examples_style": "Use contexto brasileiro, WhatsApp, redes sociais locais",
                "cultural_references": "Cultura brasileira, eventos atuais do Brasil"
            }
        }
    
    def _get_portugal_content_templates(self) -> Dict:
        """Get content templates for Portuguese (Portugal) context."""
        return {
            ContentCategory.EXAMPLES: {
                "privacy": [
                    "Proteção de dados pessoais e RGPD",
                    "Privacidade em redes sociais europeias",
                    "Vigilância digital e direitos dos cidadãos"
                ],
                "deepfakes": [
                    "Vídeos manipulados de figuras públicas portuguesas",
                    "Deepfakes em contexto europeu",
                    "Notícias falsas com conteúdo audiovisual"
                ],
                "social_media": [
                    "Desinformação em grupos de Facebook portugueses",
                    "Golpes digitais em Portugal",
                    "Fake news em plataformas europeias"
                ]
            },
            ContentCategory.DISINFORMATION_PATTERNS: {
                "health": {
                    "common_topics": ["desinformação sobre saúde", "teorias alternativas", "SNS e vacinas"],
                    "platforms": ["Facebook", "WhatsApp", "Twitter"],
                    "red_flags": ["Fontes não verificadas", "Linguagem alarmista", "Anti-ciência"]
                },
                "politics": {
                    "common_topics": ["desinformação política", "União Europeia", "questões nacionais"],
                    "platforms": ["Facebook", "Twitter", "WhatsApp"],
                    "red_flags": ["Extremismo político", "Fontes duvidosas", "Manipulação de factos"]
                }
            },
            ContentCategory.SCENARIOS: {
                "catfish": [
                    {
                        "difficulty": 1,
                        "description": "Pessoa com perfil falso em redes sociais",
                        "red_flags": ["Evita encontros presenciais", "Pede dinheiro", "Informações contraditórias"],
                        "platform": "Redes sociais"
                    }
                ]
            },
            ContentCategory.COMMUNICATION_STYLES: {
                "tone": "educado e profissional",
                "formality": "formal-moderado",
                "examples_style": "Use contexto português e europeu",
                "cultural_references": "Cultura portuguesa, eventos europeus"
            }
        }
    
    def _get_default_scenario(self, cultural_context: CulturalContext) -> Dict:
        """Get default scenario if specific one not found."""
        return {
            "difficulty": 1,
            "description": "Generic social media scenario",
            "red_flags": ["Suspicious behavior", "Requests for personal information"],
            "platform": "Social media"
        }

    def adapt_content_for_culture(
        self,
        content: str,
        source_context: CulturalContext,
        target_context: CulturalContext
    ) -> str:
        """
        Adapt content from one cultural context to another.
        
        Args:
            content: Original content
            source_context: Source cultural context
            target_context: Target cultural context
            
        Returns:
            Adapted content
        """
        # This is a placeholder for more sophisticated adaptation
        # In production, this could use LLM-based translation and cultural adaptation
        if source_context == target_context:
            return content
        
        # Get communication styles for both contexts
        source_style = self.get_communication_style_guide(source_context)
        target_style = self.get_communication_style_guide(target_context)
        
        # Return content with adaptation note
        # In production, this would do actual content transformation
        return content
    
    def get_localized_disinformation_concerns(
        self,
        cultural_context: CulturalContext
    ) -> List[str]:
        """
        Get list of primary disinformation concerns for a culture.
        
        Args:
            cultural_context: Cultural context
            
        Returns:
            List of localized concerns
        """
        concerns = {
            CulturalContext.ENGLISH_US: [
                "Political polarization and election misinformation",
                "Health misinformation (vaccines, COVID-19)",
                "Social media manipulation and fake accounts",
                "Deepfakes and synthetic media"
            ],
            CulturalContext.ENGLISH_UK: [
                "Brexit-related misinformation",
                "NHS and health service misinformation",
                "Privacy and GDPR concerns",
                "Political disinformation"
            ],
            CulturalContext.PORTUGUESE_BRAZIL: [
                "Correntes de WhatsApp com fake news",
                "Desinformação política e eleitoral",
                "Golpes financeiros em redes sociais",
                "Notícias falsas sobre saúde e vacinas"
            ],
            CulturalContext.PORTUGUESE_PORTUGAL: [
                "Desinformação sobre União Europeia",
                "Proteção de dados e RGPD",
                "Fake news em contexto português",
                "Golpes digitais e fraudes online"
            ]
        }
        return concerns.get(cultural_context, concerns[CulturalContext.ENGLISH_US])
    
    def get_platform_preferences(
        self,
        cultural_context: CulturalContext
    ) -> List[str]:
        """
        Get preferred social media platforms for a culture.
        
        Args:
            cultural_context: Cultural context
            
        Returns:
            List of platform names in order of popularity
        """
        platforms = {
            CulturalContext.ENGLISH_US: [
                "Facebook", "Instagram", "Twitter/X", "TikTok", "YouTube"
            ],
            CulturalContext.ENGLISH_UK: [
                "Facebook", "WhatsApp", "Instagram", "Twitter", "YouTube"
            ],
            CulturalContext.PORTUGUESE_BRAZIL: [
                "WhatsApp", "Instagram", "Facebook", "TikTok", "YouTube"
            ],
            CulturalContext.PORTUGUESE_PORTUGAL: [
                "Facebook", "WhatsApp", "Instagram", "YouTube", "Twitter"
            ]
        }
        return platforms.get(cultural_context, platforms[CulturalContext.ENGLISH_US])


# Singleton instance
_cultural_content_service: Optional[CulturalContentService] = None


def get_cultural_content_service() -> CulturalContentService:
    """Get singleton instance of cultural content service."""
    global _cultural_content_service
    if _cultural_content_service is None:
        _cultural_content_service = CulturalContentService()
    return _cultural_content_service
