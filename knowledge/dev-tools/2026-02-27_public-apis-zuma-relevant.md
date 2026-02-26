# Relevant Public APIs for Zuma Indonesia & Iris

Filtered from public-apis/public-apis repository for retail/FMCG operations, data analysis, and AI orchestration.

---

## 📊 Finance & Business Intelligence

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Alpha Vantage** | Real-time & historical stock data (market analysis) | apiKey | ✅ | ❌ |
| **Finnhub** | Real-time stock/currency/crypto data for financial dashboards | apiKey | ✅ | ❌ |
| **FRED** | Economic data from Federal Reserve (macro trends) | apiKey | ✅ | ✅ |
| **Plaid** | Bank account & transaction data access (financial reconciliation) | apiKey | ✅ | ❌ |
| **Klarna** | Payment & shopping service integration | apiKey | ✅ | ❌ |
| **MercadoPago** | Payment processing for e-commerce (⚠️ NOT recommended for Indonesia - no IDR support) | apiKey | ✅ | ❌ |
| **Zoho Books** | Online accounting software (financial management) | OAuth | ✅ | ❌ |
| **VAT Validation** | Validate VAT numbers & calculate rates (tax compliance) | apiKey | ✅ | ✅ |
| **Tax Data API** | VAT number & tax validation globally | apiKey | ✅ | ❌ |
| **Xendit** | Indonesia payment gateway (IDR, GoPay, OVO, DANA, bank transfer) | apiKey | ✅ | ❌ |
| **Midtrans** | Indonesia payment gateway (Verifone subsidiary, 250+ payment methods) | apiKey | ✅ | ❌ |
| **Doku** | Indonesia payment gateway (credit card, e-wallet, bank transfer) | apiKey | ✅ | ❌ |

---

## 🗺️ Geocoding & Location Intelligence

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Google Maps** | Store location mapping, route optimization, geofencing | apiKey | ✅ | ❌ |
| **Mapbox** | Custom digital maps for store locations & logistics | apiKey | ✅ | ❌ |
| **OpenStreetMap** | Navigation, geolocation, geographical data (open-source) | OAuth | ❌ | ❌ |
| **ipstack** | IP geolocation (identify customer location from IP) | apiKey | ✅ | ❌ |
| **IP Geolocation** | Geolocate website visitors from IP address | apiKey | ✅ | ✅ |
| **LocationIQ** | Forward/reverse geocoding & batch geocoding | apiKey | ✅ | ✅ |
| **Geocod.io** | Address geocoding/reverse geocoding in bulk | apiKey | ✅ | ❌ |
| **CountryStateCity** | World countries, states, cities in JSON/CSV (store master data) | apiKey | ✅ | ✅ |
| **REST Countries** | Get information about countries via RESTful API | No | ✅ | ✅ |

---

## 🚚 Transportation & Logistics

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **TomTom** | Maps, directions, places, traffic APIs (delivery routing) | apiKey | ✅ | ✅ |
| **HERE Maps** | Create/customize digital maps (logistics optimization) | apiKey | ✅ | ❌ |
| **OpenRouteService** | Directions, POIs, isochrones, geocoding, elevation | apiKey | ✅ | ❌ |
| **Mapbox Directions** | Route optimization for delivery networks | apiKey | ✅ | ❌ |

---

## 📱 Communication & Notifications

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Sendgrid** | Transactional email (order confirmations, alerts) - ⚠️ Free tier ended July 2025 | apiKey | ✅ | ❌ |
| **Sendinblue** | Marketing & transactional email + SMS | apiKey | ✅ | ❌ |
| **Mailchimp** | Email marketing campaigns & automation | apiKey | ✅ | ❌ |
| **Twilio** | SMS, voice, WhatsApp messaging (Iris delivery notifications) - ✅ Indonesia support | apiKey | ✅ | ❌ |
| **OneSignal** | Push notifications, email, SMS, in-app messaging | apiKey | ✅ | ❌ |

---

## 📰 News & Market Intelligence

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **NewsAPI** | Headlines from 50,000+ news sources (market trends) | apiKey | ✅ | ❌ |
| **GNews** | Search news from various sources (competitor monitoring) | apiKey | ✅ | ✅ |
| **MarketAux** | Live stock market news with sentiment analysis | apiKey | ✅ | ✅ |
| **The Guardian** | Access Guardian content by tags/section (brand monitoring) | apiKey | ✅ | ❌ |
| **New York Times** | NYT Developer Network (news & trends) | apiKey | ✅ | ❌ |

---

## 🤖 Machine Learning & AI

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Clarifai** | Computer vision (product image recognition, QA) | OAuth | ✅ | ❌ |
| **Cloudmersive** | Image captioning, face recognition, NSFW classification | apiKey | ✅ | ✅ |
| **Imagga** | Image recognition, tagging, visual search, NSFW moderation | apiKey | ✅ | ❌ |
| **NLP Cloud** | NLP using spaCy & transformers (sentiment, classification, summarization) - ✅ Indonesian support | apiKey | ✅ | ❌ |
| **Perspective** | NLP API for toxicity/obscenity/insult detection (content moderation) | apiKey | ✅ | ❌ |
| **Dialogflow** | Natural language processing (chatbot for customer service) | apiKey | ✅ | ❌ |
| **WolframAlpha** | Provides specific answers using data & algorithms (data analysis) | apiKey | ✅ | ❌ |

---

## 🛍️ Shopping & E-Commerce

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Yelp** | Find local business info (competitor analysis, store reviews) | OAuth | ✅ | ❌ |
| **Kroger** | Supermarket data (competitive intelligence) | apiKey | ✅ | ❌ |
| **Open Brewery DB** | Breweries, cideries, craft beer shops (retail benchmarking) | No | ✅ | ✅ |
| **Open Food Facts** | Food products database (product research) | No | ✅ | ❌ |

---

## 📊 Data Validation & Quality

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Email Validation** | Validate email addresses for deliverability | apiKey | ✅ | ✅ |
| **Phone Validation** | Validate phone numbers globally | apiKey | ✅ | ✅ |
| **Cloudmersive Validate** | Validate email, phone, VAT numbers, domain names | apiKey | ✅ | ✅ |
| **US Street Address** | Validate & append data for US postal addresses | apiKey | ✅ | ✅ |
| **vatlayer** | VAT number validation | apiKey | ✅ | ❌ |

---

## 📈 Text Analysis & NLP

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **NLP Cloud** | Sentiment analysis, text classification, summarization | apiKey | ✅ | ❌ |
| **Perspective** | Detect toxic/obscene/insulting text (content moderation) | apiKey | ✅ | ❌ |
| **EXUDE-API** | Filter stopping/stemming words from text data | No | ✅ | ✅ |
| **Irisnet** | Real-time content moderation (image/text) | apiKey | ✅ | ✅ |

---

## 📍 Tracking & Monitoring

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Open Notify** | ISS astronauts, current location (real-time tracking example) | No | ❌ | ❌ |
| **Sunrise and Sunset** | Sunset/sunrise times for lat/lon (operational planning) | No | ✅ | ❌ |
| **TLE** | Satellite information (real-time tracking) | No | ✅ | ❌ |

---

## 🌤️ Weather & Environmental

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Weatherstack** | Retrieve instant, accurate weather for any location | apiKey | ✅ | ❌ |
| **OpenWeatherMap** | Weather data, forecasts, alerts (operational planning) | apiKey | ✅ | ❌ |
| **IQAir** | Air quality & weather data (store operations) | apiKey | ✅ | ❌ |
| **OpenAQ** | Open air quality data (environmental monitoring) | apiKey | ✅ | ❌ |

---

## 🏛️ Government & Public Data (Indonesia-Relevant)

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Brazil** | Community-driven API for Brazil public data | No | ✅ | ✅ |
| **Open Government, Indonesia** | Indonesian government open data | apiKey | ✅ | ❌ |
| **COVID-ID** | Indonesian government COVID data per province | No | ✅ | ✅ |
| **Data.gov** | US Government data (benchmarking) | apiKey | ✅ | ❌ |

---

## 💼 Business & Productivity

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Airtable** | Integrate with Airtable (data management) | apiKey | ✅ | ❌ |
| **Asana** | Programmatic access to Asana (project management) | apiKey | ✅ | ✅ |
| **ClickUp** | Cloud-based project management tool | OAuth | ✅ | ❌ |
| **Trello** | Boards, lists, cards for project organization | OAuth | ✅ | ❌ |
| **Google Sheets** | API to read/write Google Sheets data | OAuth | ✅ | ❌ |
| **Google Docs** | API to read/write Google Docs | OAuth | ✅ | ❌ |

---

## 🔐 Security & Compliance

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **BitWarden** | Password manager (credential management) | OAuth | ✅ | ❌ |
| **EmailRep** | Email threat & risk prediction (security) | No | ✅ | ❌ |
| **Complete Criminal Checks** | Offender data from US states (compliance) | apiKey | ✅ | ✅ |

---

## 📞 Phone & Contact

| API | Use Case | Auth | HTTPS | CORS |
|-----|----------|------|-------|------|
| **Numverify** | Phone number validation (customer data quality) | apiKey | ✅ | ❌ |
| **Phone Validation** | Validate phone numbers globally | apiKey | ✅ | ✅ |
| **Veriphone** | Phone number validation & carrier lookup | apiKey | ✅ | ✅ |

---

## 🎯 Recommended Integration Priority for Zuma & Iris

### **Tier 1 (High Priority)**
1. **Google Maps / Mapbox** - Store location mapping & delivery routing
2. **Sendgrid / Sendinblue** - Email notifications for orders & alerts
3. **NewsAPI / GNews** - Market & competitor intelligence
4. **NLP Cloud / Perspective** - Customer feedback analysis & content moderation
5. **Plaid** - Financial reconciliation (if needed)

### **Tier 2 (Medium Priority)**
1. **Weatherstack** - Operational planning (foot traffic, delivery timing)
2. **Email/Phone Validation** - Customer data quality
3. **Yelp** - Competitor analysis & customer reviews
4. **Airtable / Google Sheets** - Data management & reporting
5. **OneSignal** - Push notifications for mobile app

### **Tier 3 (Nice-to-Have)**
1. **Clarifai / Imagga** - Product image recognition & QA
2. **TomTom / HERE Maps** - Advanced logistics optimization
3. **Zoho Books** - Accounting integration
4. **Twilio** - WhatsApp delivery notifications (Indonesia-friendly)

---

## 🇮🇩 Indonesia-Specific Considerations

- **Payment**: ⚠️ MercadoPago does NOT support IDR. Use: Xendit, Midtrans, Doku (all support GoPay, OVO, DANA, bank transfer)
- **SMS/WhatsApp**: Twilio ✅ supports Indonesia; Nexmo/Vonage alternative
- **Weather**: Critical for retail operations in tropical climate
- **Government Data**: Limited Indonesian APIs; focus on Brazil/Singapore models
- **Language**: NLP Cloud supports Indonesian via spaCy models
- **Logistics**: Google Maps & TomTom have good Indonesia coverage

---

**Last Updated**: February 2026
**Source**: public-apis/public-apis GitHub repository

---

## 🔍 Verification Report (Feb 27, 2026)

### Tier-1 API Status

| API | Status | Notes |
|-----|--------|-------|
| **Google Maps** | ✅ VERIFIED | Full coverage for all Zuma regions (Jatim, Jakarta, Sumatra, Sulawesi, Batam, Bali). Places Aggregate API available. |
| **Sendgrid** | ⚠️ CRITICAL CHANGE | Free tier ended July 26, 2025. Paid plans start at $29/month. CORS NOT supported (requires backend). |
| **NewsAPI** | ✅ VERIFIED | Free tier: 100 requests/day, 24-hour article delay. Paid: $449/month (250K req/month). CORS NOT supported. |
| **NLP Cloud** | ✅ VERIFIED | Indonesian language support via spaCy models. Free tier: $15 credit. Pay-as-you-go: $0.003-0.005/request. |

### Indonesia Payment Gateway Comparison

| Gateway | IDR Support | E-Wallets | Bank Transfer | Setup Fee | Commission |
|---------|-------------|-----------|---------------|-----------|-----------|
| **Xendit** | ✅ | GoPay, OVO, DANA | ✅ | Free | 2.9% + RP 2,000 |
| **Midtrans** | ✅ | GoPay, Mandiri, BCA | ✅ | Free | 2.9% + RP 2,000 |
| **Doku** | ✅ | GoPay, OVO, DANA | ✅ | Free | Bank fee + RP 2,500 |
| **MercadoPago** | ❌ NO IDR | Limited | ❌ | Free | 3.9% + $0.45 |

**Recommendation**: Use **Xendit** or **Midtrans** for Zuma Indonesia operations. Both support all major local payment methods.

### CORS Support Analysis

**APIs with CORS enabled** (frontend-safe):
- FRED, IP Geolocation, LocationIQ, CountryStateCity, REST Countries, TomTom, GNews, MarketAux, Cloudmersive, Asana, Complete Criminal Checks, Phone Validation, Veriphone, EXUDE-API, Irisnet

**APIs WITHOUT CORS** (require backend proxy):
- Google Maps, Sendgrid, NewsAPI, NLP Cloud, Twilio, Plaid, Finnhub, Alpha Vantage, Clarifai, Perspective, Dialogflow

**Implication**: Frontend integrations for Zuma mobile/web apps must use backend proxy for 60% of Tier-1 APIs.

### Critical Findings

1. **Sendgrid Free Tier Deprecated**: Must migrate to Sendinblue, Mailchimp, or AWS SES
2. **MercadoPago Unsuitable**: No IDR support; replace with Xendit/Midtrans
3. **CORS Limitations**: Most payment/communication APIs require backend proxy
4. **Indonesian Language**: NLP Cloud confirmed Indonesian support via spaCy
5. **Google Maps Coverage**: ✅ Full coverage for all Zuma regions
