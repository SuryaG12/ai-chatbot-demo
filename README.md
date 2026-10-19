# AI Chatbot for Local Businesses - Demo

A working starter version of a product to sell to local businesses: an
embeddable chat widget for their website that answers customer questions
from an FAQ file and captures leads when it does not know an answer.

## What's here

- `backend/app.py` - FastAPI server. Serves the demo page, the `/chat`
  endpoint (keyword matching against the FAQ), and `/leads` (captured leads).
- `backend/business_faq.json` - the "brain". One file per client: their
  business name, FAQs, and fallback message. **This is the only file you
  change per client.**
- `backend/business_faq_auto.json` - a second sample business
  ("Eastside Auto Care", 8 FAQs). Useful when a prospect asks
  "show me one for my kind of business."
- `backend/demo.html` - a sample business website with the widget installed.
- `widget/chat-widget.js` + `widget/chat-widget.css` - the embeddable chat
  bubble. A real client adds ONE script tag to their site. No rebuild needed.

## Run the demo

```bash
cd ai-chatbot-demo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend
python -m uvicorn app:app --reload --port 8000
```

Open http://localhost:8000 and click the chat bubble. Try:
- "What are your hours?" (answered from FAQ)
- "Do you whiten toenails?" (not in FAQ -> asks for contact info -> saved as a lead)

Check captured leads at http://localhost:8000/leads

To run the auto repair demo instead:

```bash
FAQ_FILE=business_faq_auto.json python -m uvicorn app:app --reload --port 8000
```

Any FAQ file in `backend/` works this way; the default is `business_faq.json`.

## Selling it to a real client

1. Copy this folder, rename it for the client.
2. Edit `business_faq.json`: their business name, 10-20 real FAQs
   (hours, location, pricing, services, booking). Get these from their
   website plus a 15-minute call with the owner.
3. Change the colors in `chat-widget.css` to match their brand.
4. Deploy the backend (Render/Railway free tier works), give them the one
   `<script>` tag to paste into their site.
5. Show them `/leads` so they see the customer contact info it collects.

## Upgrade path (later, when a client pays)

Right now answers come from keyword matching, which costs $0 and is
honest about what it knows. When you want smarter answers, add an LLM
call in `app.py`'s `/chat` endpoint: send the user question plus the FAQ
file as context to any LLM API and return its answer. Keep the keyword
version as the fallback so it never hallucinates prices or hours.

## License

MIT - see LICENSE.
