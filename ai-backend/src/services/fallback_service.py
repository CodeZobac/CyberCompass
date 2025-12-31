"""
Fallback service for AI service failures.

This module provides static educational content and alternative challenge types
when AI services are unavailable, ensuring graceful degradation of functionality.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

from ..utils.exceptions import AIServiceError
from ..utils.error_handler import logger


class FallbackContentType(str, Enum):
    """Types of fallback content available."""
    FEEDBACK = "feedback"
    DEEPFAKE_CHALLENGE = "deepfake_challenge"
    SOCIAL_MEDIA_POST = "social_media_post"
    CATFISH_RESPONSE = "catfish_response"
    ANALYTICS = "analytics"


class FallbackService:
    """
    Service providing fallback content when AI services are unavailable.
    
    This service maintains a library of pre-generated educational content
    that can be served when CrewAI agents or LLM services fail.
    """
    
    def __init__(self):
        self.fallback_content = self._initialize_fallback_content()
        self.usage_count: Dict[str, int] = {}
    
    def _initialize_fallback_content(self) -> Dict[str, Any]:
        """Initialize static fallback content library."""
        return {
            "feedback": {
                "en": self._get_english_feedback_templates(),
                "pt": self._get_portuguese_feedback_templates()
            },
            "deepfake_challenges": {
                "en": self._get_english_deepfake_challenges(),
                "pt": self._get_portuguese_deepfake_challenges()
            },
            "social_media_posts": {
                "en": self._get_english_social_media_posts(),
                "pt": self._get_portuguese_social_media_posts()
            },
            "catfish_responses": {
                "en": self._get_english_catfish_responses(),
                "pt": self._get_portuguese_catfish_responses()
            },
            "analytics": {
                "en": self._get_english_analytics_messages(),
                "pt": self._get_portuguese_analytics_messages()
            }
        }
    
    def get_fallback_feedback(
        self,
        locale: str = "en",
        challenge_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get fallback feedback when AI feedback generation fails.
        
        Args:
            locale: Language locale (en or pt)
            challenge_type: Optional challenge type for context
        
        Returns:
            Fallback feedback response
        """
        logger.warning(
            "Using fallback feedback",
            locale=locale,
            challenge_type=challenge_type
        )
        
        self._increment_usage("feedback", locale)
        
        templates = self.fallback_content["feedback"].get(locale, self.fallback_content["feedback"]["en"])
        
        # Select appropriate template based on challenge type
        if challenge_type and challenge_type in templates:
            template = templates[challenge_type]
        else:
            template = templates.get("general", templates[list(templates.keys())[0]])
        
        return {
            "feedback": template["message"],
            "reasoning": template["reasoning"],
            "learning_objectives": template["learning_objectives"],
            "follow_up_questions": template["follow_up_questions"],
            "is_fallback": True,
            "fallback_reason": "AI service temporarily unavailable"
        }
    
    def get_fallback_deepfake_challenge(self, locale: str = "en") -> Dict[str, Any]:
        """
        Get fallback deepfake challenge when AI generation fails.
        
        Args:
            locale: Language locale (en or pt)
        
        Returns:
            Fallback deepfake challenge
        """
        logger.warning("Using fallback deepfake challenge", locale=locale)
        
        self._increment_usage("deepfake_challenge", locale)
        
        challenges = self.fallback_content["deepfake_challenges"].get(
            locale,
            self.fallback_content["deepfake_challenges"]["en"]
        )
        
        # Rotate through challenges based on usage
        index = self.usage_count.get(f"deepfake_challenge_{locale}", 0) % len(challenges)
        challenge = challenges[index]
        
        return {
            **challenge,
            "is_fallback": True,
            "fallback_reason": "AI service temporarily unavailable"
        }
    
    def get_fallback_social_media_post(self, locale: str = "en") -> Dict[str, Any]:
        """
        Get fallback social media post when AI generation fails.
        
        Args:
            locale: Language locale (en or pt)
        
        Returns:
            Fallback social media post
        """
        logger.warning("Using fallback social media post", locale=locale)
        
        self._increment_usage("social_media_post", locale)
        
        posts = self.fallback_content["social_media_posts"].get(
            locale,
            self.fallback_content["social_media_posts"]["en"]
        )
        
        index = self.usage_count.get(f"social_media_post_{locale}", 0) % len(posts)
        post = posts[index]
        
        return {
            **post,
            "is_fallback": True,
            "fallback_reason": "AI service temporarily unavailable"
        }
    
    def get_fallback_catfish_response(
        self,
        user_message: str,
        locale: str = "en"
    ) -> Dict[str, Any]:
        """
        Get fallback catfish response when AI conversation fails.
        
        Args:
            user_message: User's message
            locale: Language locale (en or pt)
        
        Returns:
            Fallback catfish response
        """
        logger.warning(
            "Using fallback catfish response",
            locale=locale,
            user_message_length=len(user_message)
        )
        
        self._increment_usage("catfish_response", locale)
        
        responses = self.fallback_content["catfish_responses"].get(
            locale,
            self.fallback_content["catfish_responses"]["en"]
        )
        
        # Select response based on message content
        response = self._select_contextual_response(user_message, responses)
        
        return {
            "message": response["text"],
            "typing_delay": 2.0,
            "red_flags": response.get("red_flags", []),
            "is_fallback": True,
            "fallback_reason": "AI service temporarily unavailable"
        }
    
    def get_fallback_analytics(self, locale: str = "en") -> Dict[str, Any]:
        """
        Get fallback analytics message when AI analytics fails.
        
        Args:
            locale: Language locale (en or pt)
        
        Returns:
            Fallback analytics message
        """
        logger.warning("Using fallback analytics", locale=locale)
        
        self._increment_usage("analytics", locale)
        
        messages = self.fallback_content["analytics"].get(
            locale,
            self.fallback_content["analytics"]["en"]
        )
        
        return {
            "message": messages["unavailable"],
            "is_fallback": True,
            "fallback_reason": "AI service temporarily unavailable"
        }
    
    def _increment_usage(self, content_type: str, locale: str):
        """Track fallback content usage."""
        key = f"{content_type}_{locale}"
        self.usage_count[key] = self.usage_count.get(key, 0) + 1
    
    def _select_contextual_response(
        self,
        user_message: str,
        responses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Select most appropriate response based on user message."""
        user_message_lower = user_message.lower()
        
        # Simple keyword matching for context
        for response in responses:
            if any(keyword in user_message_lower for keyword in response.get("keywords", [])):
                return response
        
        # Default to first response
        return responses[0]
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get fallback usage statistics for monitoring."""
        return {
            "usage_count": self.usage_count,
            "total_fallbacks": sum(self.usage_count.values()),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Content template methods
    def _get_english_feedback_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get English feedback templates."""
        return {
            "general": {
                "message": "Thank you for your response. Ethical decision-making requires careful consideration of multiple perspectives and potential consequences.",
                "reasoning": "In cyber ethics, there are often no simple right or wrong answers. The best approach involves weighing the interests of all stakeholders, considering both immediate and long-term impacts, and adhering to established ethical principles.",
                "learning_objectives": [
                    "Understand the complexity of ethical dilemmas",
                    "Consider multiple stakeholder perspectives",
                    "Evaluate consequences of decisions"
                ],
                "follow_up_questions": [
                    "What other stakeholders might be affected by this decision?",
                    "What are the potential long-term consequences?",
                    "How might cultural context influence this ethical decision?"
                ]
            },
            "privacy": {
                "message": "Privacy is a fundamental right in the digital age. Your response shows consideration for data protection principles.",
                "reasoning": "Privacy decisions require balancing individual rights with organizational needs and legal requirements. Best practices include data minimization, transparency, and user consent.",
                "learning_objectives": [
                    "Understand privacy principles",
                    "Apply data protection best practices",
                    "Balance competing interests"
                ],
                "follow_up_questions": [
                    "How can organizations be transparent about data collection?",
                    "What are the risks of inadequate privacy protection?",
                    "How do privacy laws vary across jurisdictions?"
                ]
            }
        }
    
    def _get_portuguese_feedback_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get Portuguese feedback templates."""
        return {
            "general": {
                "message": "Obrigado pela sua resposta. A tomada de decisões éticas requer consideração cuidadosa de múltiplas perspectivas e consequências potenciais.",
                "reasoning": "Na ética cibernética, muitas vezes não há respostas simples de certo ou errado. A melhor abordagem envolve ponderar os interesses de todas as partes interessadas, considerar impactos imediatos e de longo prazo, e aderir a princípios éticos estabelecidos.",
                "learning_objectives": [
                    "Compreender a complexidade dos dilemas éticos",
                    "Considerar múltiplas perspectivas das partes interessadas",
                    "Avaliar as consequências das decisões"
                ],
                "follow_up_questions": [
                    "Que outras partes interessadas podem ser afetadas por esta decisão?",
                    "Quais são as potenciais consequências a longo prazo?",
                    "Como o contexto cultural pode influenciar esta decisão ética?"
                ]
            },
            "privacy": {
                "message": "A privacidade é um direito fundamental na era digital. Sua resposta mostra consideração pelos princípios de proteção de dados.",
                "reasoning": "As decisões de privacidade exigem equilibrar direitos individuais com necessidades organizacionais e requisitos legais. As melhores práticas incluem minimização de dados, transparência e consentimento do usuário.",
                "learning_objectives": [
                    "Compreender os princípios de privacidade",
                    "Aplicar as melhores práticas de proteção de dados",
                    "Equilibrar interesses concorrentes"
                ],
                "follow_up_questions": [
                    "Como as organizações podem ser transparentes sobre a coleta de dados?",
                    "Quais são os riscos de proteção inadequada da privacidade?",
                    "Como as leis de privacidade variam entre jurisdições?"
                ]
            }
        }

    
    def _get_english_deepfake_challenges(self) -> List[Dict[str, Any]]:
        """Get English deepfake challenge templates."""
        return [
            {
                "challenge_id": "fallback_deepfake_1",
                "title": "Audio Deepfake Detection",
                "description": "Listen to this audio clip and determine if it's authentic or a deepfake.",
                "media_type": "audio",
                "difficulty": "beginner",
                "detection_clues": [
                    "Unnatural pauses or rhythm",
                    "Inconsistent background noise",
                    "Robotic or synthesized quality"
                ],
                "educational_content": "Deepfakes use AI to create realistic but fake audio or video. Listen carefully for unnatural patterns, inconsistencies, or artifacts that might indicate manipulation."
            },
            {
                "challenge_id": "fallback_deepfake_2",
                "title": "Video Deepfake Detection",
                "description": "Watch this video and identify signs of deepfake manipulation.",
                "media_type": "video",
                "difficulty": "intermediate",
                "detection_clues": [
                    "Facial movements don't match speech",
                    "Blurring around face edges",
                    "Unnatural eye movements or blinking"
                ],
                "educational_content": "Video deepfakes often show subtle inconsistencies in facial movements, lighting, or synchronization. Pay attention to details like eye contact, lip sync, and edge artifacts."
            }
        ]
    
    def _get_portuguese_deepfake_challenges(self) -> List[Dict[str, Any]]:
        """Get Portuguese deepfake challenge templates."""
        return [
            {
                "challenge_id": "fallback_deepfake_1_pt",
                "title": "Detecção de Deepfake de Áudio",
                "description": "Ouça este clipe de áudio e determine se é autêntico ou um deepfake.",
                "media_type": "audio",
                "difficulty": "beginner",
                "detection_clues": [
                    "Pausas ou ritmo não naturais",
                    "Ruído de fundo inconsistente",
                    "Qualidade robótica ou sintetizada"
                ],
                "educational_content": "Deepfakes usam IA para criar áudio ou vídeo realista, mas falso. Ouça atentamente padrões não naturais, inconsistências ou artefatos que possam indicar manipulação."
            },
            {
                "challenge_id": "fallback_deepfake_2_pt",
                "title": "Detecção de Deepfake de Vídeo",
                "description": "Assista a este vídeo e identifique sinais de manipulação deepfake.",
                "media_type": "video",
                "difficulty": "intermediate",
                "detection_clues": [
                    "Movimentos faciais não correspondem à fala",
                    "Desfoque nas bordas do rosto",
                    "Movimentos oculares ou piscadas não naturais"
                ],
                "educational_content": "Deepfakes de vídeo frequentemente mostram inconsistências sutis em movimentos faciais, iluminação ou sincronização. Preste atenção a detalhes como contato visual, sincronia labial e artefatos de borda."
            }
        ]
    
    def _get_english_social_media_posts(self) -> List[Dict[str, Any]]:
        """Get English social media post templates."""
        return [
            {
                "post_id": "fallback_post_1",
                "content": "BREAKING: New study shows shocking health risks! Share before it's deleted!",
                "author": "HealthNewsDaily",
                "is_disinformation": True,
                "red_flags": [
                    "Urgency and fear tactics",
                    "Vague claims without sources",
                    "Request to share before verification"
                ],
                "educational_note": "This post uses common disinformation tactics: creating urgency, making vague claims, and encouraging rapid sharing without verification."
            },
            {
                "post_id": "fallback_post_2",
                "content": "According to a peer-reviewed study published in Nature, researchers found... [link to study]",
                "author": "ScienceDaily",
                "is_disinformation": False,
                "red_flags": [],
                "educational_note": "This post shows signs of credible information: cites specific sources, links to original research, and uses measured language."
            }
        ]
    
    def _get_portuguese_social_media_posts(self) -> List[Dict[str, Any]]:
        """Get Portuguese social media post templates."""
        return [
            {
                "post_id": "fallback_post_1_pt",
                "content": "URGENTE: Novo estudo mostra riscos chocantes para a saúde! Compartilhe antes que seja deletado!",
                "author": "NotíciasSaúdeDiária",
                "is_disinformation": True,
                "red_flags": [
                    "Urgência e táticas de medo",
                    "Alegações vagas sem fontes",
                    "Pedido para compartilhar antes da verificação"
                ],
                "educational_note": "Esta postagem usa táticas comuns de desinformação: criar urgência, fazer alegações vagas e encorajar compartilhamento rápido sem verificação."
            },
            {
                "post_id": "fallback_post_2_pt",
                "content": "De acordo com um estudo revisado por pares publicado na Nature, pesquisadores descobriram... [link para o estudo]",
                "author": "CiênciaHoje",
                "is_disinformation": False,
                "red_flags": [],
                "educational_note": "Esta postagem mostra sinais de informação credível: cita fontes específicas, links para pesquisa original e usa linguagem moderada."
            }
        ]
    
    def _get_english_catfish_responses(self) -> List[Dict[str, Any]]:
        """Get English catfish response templates."""
        return [
            {
                "text": "Hey! Sorry for the late reply, I've been super busy with work stuff.",
                "keywords": ["hi", "hello", "hey", "how are you"],
                "red_flags": ["Vague about personal details"]
            },
            {
                "text": "I'd love to video chat but my camera is broken right now. Maybe we can just keep texting?",
                "keywords": ["video", "call", "facetime", "meet"],
                "red_flags": ["Avoids video calls", "Makes excuses"]
            },
            {
                "text": "I'm 25 and work in tech. What about you?",
                "keywords": ["age", "old", "work", "job"],
                "red_flags": ["Inconsistent age claims"]
            },
            {
                "text": "That's cool! I remember when that was popular back in the day.",
                "keywords": ["music", "movie", "game", "show"],
                "red_flags": ["Outdated cultural references"]
            }
        ]
    
    def _get_portuguese_catfish_responses(self) -> List[Dict[str, Any]]:
        """Get Portuguese catfish response templates."""
        return [
            {
                "text": "Oi! Desculpa a demora, estive super ocupado com coisas do trabalho.",
                "keywords": ["oi", "olá", "hey", "como vai"],
                "red_flags": ["Vago sobre detalhes pessoais"]
            },
            {
                "text": "Adoraria fazer videochamada mas minha câmera está quebrada agora. Talvez possamos continuar conversando por texto?",
                "keywords": ["video", "chamada", "facetime", "encontrar"],
                "red_flags": ["Evita videochamadas", "Faz desculpas"]
            },
            {
                "text": "Tenho 25 anos e trabalho com tecnologia. E você?",
                "keywords": ["idade", "anos", "trabalho", "emprego"],
                "red_flags": ["Alegações de idade inconsistentes"]
            },
            {
                "text": "Que legal! Lembro quando isso era popular antigamente.",
                "keywords": ["música", "filme", "jogo", "série"],
                "red_flags": ["Referências culturais desatualizadas"]
            }
        ]
    
    def _get_english_analytics_messages(self) -> Dict[str, str]:
        """Get English analytics messages."""
        return {
            "unavailable": "Analytics are temporarily unavailable. Your progress is being tracked and will be available soon.",
            "limited": "Limited analytics available. Full insights will be provided when AI services are restored."
        }
    
    def _get_portuguese_analytics_messages(self) -> Dict[str, str]:
        """Get Portuguese analytics messages."""
        return {
            "unavailable": "As análises estão temporariamente indisponíveis. Seu progresso está sendo rastreado e estará disponível em breve.",
            "limited": "Análises limitadas disponíveis. Insights completos serão fornecidos quando os serviços de IA forem restaurados."
        }


# Global fallback service instance
fallback_service = FallbackService()
