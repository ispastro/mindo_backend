import re
from groq import Groq
from ..config import settings
import traceback

# Configure Groq
client = None
if settings.GROQ_API_KEY:
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        print("✅ Groq client initialized successfully")
        print(f"🔑 API Key: {settings.GROQ_API_KEY[:20]}...")
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        print(f"Traceback: {traceback.format_exc()}")
else:
    print("⚠️ No GROQ_API_KEY found in environment variables")


STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "of", "my",
    "is", "are", "was", "were", "what", "where", "how", "did", "do",
    "i", "you", "me", "it", "this", "that", "there", "here",
    "put", "find", "show", "looking", "need", "get", "give"
}


def _local_keywords(text: str) -> str:
    """Simple fallback extractor: strip punctuation/stopwords for basic matching"""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [t for t in cleaned.split() if t and t not in STOPWORDS]
    return " ".join(tokens) if tokens else text.strip()

def extract_search_terms(natural_query: str, language: str = "auto") -> str:
    """
    Extract search terms from natural language query using Groq AI
    Supports multiple languages including Amharic, English, etc.
    
    Examples:
    - "Where are my car keys?" -> "car keys"
    - "የእኔ ቁልፍ የት ነው?" (Amharic: Where is my key?) -> "key"
    - "Find my wallet in the bedroom" -> "wallet bedroom"
    """
    print(f"🔍 extract_search_terms called with: '{natural_query}'")
    
    if not client:
        print("⚠️ No Groq client available, using local fallback")
        return _local_keywords(natural_query)
    
    # Check if query contains non-ASCII (likely Amharic or other language)
    is_non_english = any(ord(char) > 127 for char in natural_query)
    print(f"📝 Is non-English: {is_non_english}")
    
    try:
        if is_non_english:
            # Translation mode for non-English queries
            prompt = f"""
You must translate this Amharic query to English. Return ONLY the English word.

Examples:
"ቁልፍ የት ነው" -> key
"የእኔ ቁልፍ የት ነው?" -> key
"ኪስ የት አስቀመጥኩት?" -> wallet
"በኩሽና ውስጥ" -> kitchen
"ስልኬን ፈልግ" -> phone

Amharic query: {natural_query}
English translation (one word only):"""
        else:
            # Extraction mode for English queries
            prompt = f"""
Extract only the OBJECT/ITEM. Remove action words.

Examples:
"where did i put wallet" → wallet
"find my car keys" → car keys
"what's in the kitchen" → kitchen

Query: {natural_query}
Extracted:"""
        
        print(f"🤖 Sending to Groq ({'translation' if is_non_english else 'extraction'}): {natural_query}")
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a translator. Always respond with ONLY the English translation, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,  # Zero temperature for consistent translation
            max_tokens=20
        )
        
        extracted = response.choices[0].message.content.strip()
        print(f"✅ Groq returned: '{extracted}'")
        
        # If extraction failed or returned original, use fallback
        if not extracted or extracted == natural_query:
            print("⚠️ AI returned original query, using fallback")
            return _local_keywords(natural_query)
        
        return extracted
        
    except Exception as e:
        # Fallback to original query on error
        print(f"❌ AI extraction error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return _local_keywords(natural_query)
