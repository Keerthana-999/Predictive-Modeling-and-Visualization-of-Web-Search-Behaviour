import re
import pandas as pd
from collections import Counter
from data_collection import DataCollection
from urllib.parse import urlparse, parse_qs

class Sessionization:
    # -----------------------------------------
    # Default domain-category map
    # -----------------------------------------
    DEFAULT_DOMAIN_MAP = {
        # Education / Career
        "coursera.org": "Education/Career", "edx.org": "Education/Career", "mit.edu": "Education/Career",
        "wikipedia.org": "Education/Career", "arxiv.org": "Education/Career",
        "linkedin.com": "Education/Career", "indeed.com": "Education/Career", "glassdoor.com": "Education/Career",

        # Social / Entertainment
        "youtube.com": "Social/Entertainment", "netflix.com": "Social/Entertainment", "spotify.com": "Social/Entertainment",
        "facebook.com": "Social/Entertainment", "instagram.com": "Social/Entertainment", "twitter.com": "Social/Entertainment",
        "tiktok.com": "Social/Entertainment", "reddit.com": "Social/Entertainment", "whatsapp.com": "Social/Entertainment",  
        "gmail.com": "Social/Entertainment",  
        "snapchat.com": "Social/Entertainment", 

        # Shopping
        "amazon.com": "Shopping", "ebay.com": "Shopping", "walmart.com": "Shopping",
        "target.com": "Shopping", "flipkart.com": "Shopping", "aliexpress.com": "Shopping",

        # Finance
        "paypal.com": "Finance", "bankofamerica.com": "Finance", "chase.com": "Finance",
        "mint.com": "Finance", "moneycontrol.com": "Finance", "robinhood.com": "Finance",

        # Travel
        "airbnb.com": "Travel", "booking.com": "Travel", "expedia.com": "Travel", "tripadvisor.com": "Travel",
        "uber.com": "Travel", "lyft.com": "Travel", "airindia.com": "Travel"
    }
    DEFAULT_DOMAIN_MAP.update({
        # --- Reassigned Education/Career ---
        "placementdriveinsta.com": "Education/Career",
        "joinhandshake.com": "Education/Career",
        "compassgroupcareers.com": "Education/Career",

        # --- Reassigned Social/Entertainment ---
        "behance.net": "Social/Entertainment",
        "ibommatamil.com": "Social/Entertainment",

        # --- Reassigned Shopping ---
        "columbia.com": "Shopping",
        "gap.com": "Shopping",
        "rakuten.com": "Shopping",

        # --- Reassigned Finance ---
        "groww.in": "Finance",

        # --- Reassigned Travel / Gov Services ---
        "sarathi.parivahan.gov.in": "Travel",
        "mymva.maryland.gov": "Travel",
        "i94.cbp.dhs.gov": "Travel",

        # --- Authentication & Portal URLs — map to nearest intent (Education or Finance) ---
        "login.gov": "Finance",           # secure access → financial/government account
        "duosecurity.com": "Education/Career",  # used in academic or workplace login portals
        "id.me": "Finance",               # identity verification for benefits & tax portals
        "ssa.gov": "Finance",             # Social Security Administration
        "cashnet.com": "Finance",         # payment gateway
        "blackthorn.io": "Education/Career", # event management for universities
        "gamma.app": "Education/Career"   # presentation tool used in academic/tech settings
    })

    # Keyword patterns
    KW_EDU = r"(edu|course|university|school|study|lecture|assignment|research|paper|thesis|arxiv|wikipedia|tutorial|how to)"
    KW_SOCIAL = r"(youtube|music|video|song|movie|stream|netflix|instagram|facebook|tiktok|reddit|meme|social|chat|streaming)"
    KW_SHOP = r"(buy|price|buying|shop|sale|discount|coupon|deal|order|cart|product|review|amazon|ebay|store)"
    KW_FIN = r"(bank|loan|account|credit|debit|investment|stock|shares|finance|tax|mortgage|broker|insurance|paypal|wallet)"
    KW_TRAVEL = r"(flight|hotel|booking|train|bus|ticket|trip|travel|airbnb|expedia|itinerary|destination)"
    KW_MISC = r"(login|settings|help|support|cdn|static|ads|analytics|localhost)"

    SEARCH_ENGINES = ("google.", "bing.", "yahoo.", "duckduckgo.", "baidu.", "yandex.")

    # -----------------------------------------
    # Helper Functions
    # -----------------------------------------
    @staticmethod
    def extract_search_query_from_url(url):
        """Extract search query if the URL is from a search engine."""
        try:
            parsed = urlparse(url or "")
            netloc = (parsed.netloc or "").lower()
            if any(s in netloc for s in Sessionization.SEARCH_ENGINES):
                qs = parse_qs(parsed.query)
                for k in ("q", "query", "p", "search"):
                    if k in qs and qs[k]:
                        return " ".join(qs[k]).lower()
                path_tokens = parsed.path.replace("/", " ").lower()
                return path_tokens.strip()
        except Exception:
            pass
        return None

    @staticmethod
    def normalize_domain(url_or_domain):
        """Return clean base domain."""
        try:
            p = urlparse(url_or_domain if "://" in url_or_domain else "http://" + url_or_domain)
            dom = p.netloc.lower()
            if dom.startswith("www."):
                dom = dom[4:]
            dom = dom.split(":")[0]
            return dom
        except Exception:
            return (url_or_domain or "").lower()

    @staticmethod
    def categorize_domain_from_url(url):
        """Categorize URLs into predefined intent categories (handles subdomains and google queries)."""
        if pd.isna(url) or str(url).strip() == "":
            return "Miscellaneous"

        url = str(url).strip()
        dom = Sessionization.normalize_domain(url)
        dom_clean = re.sub(r"^(web|mail|m|news|blog|app|en|home)\.", "", dom)

        # 1️⃣ Domain-level lookup (subdomain-aware)
        for known_domain, cat in Sessionization.DEFAULT_DOMAIN_MAP.items():
            if known_domain in dom_clean:
                return cat

        # 2️⃣ Handle Google and other search engine URLs
        if any(se in dom_clean for se in Sessionization.SEARCH_ENGINES):
            query_text = Sessionization.extract_search_query_from_url(url)
            if query_text:
                q = query_text.lower()
                if re.search(Sessionization.KW_EDU, q):
                    return "Education/Career"
                if re.search(Sessionization.KW_SOCIAL, q):
                    return "Social/Entertainment"
                if re.search(Sessionization.KW_SHOP, q):
                    return "Shopping"
                if re.search(Sessionization.KW_FIN, q):
                    return "Finance"
                if re.search(Sessionization.KW_TRAVEL, q):
                    return "Travel"
                # if no intent keyword match
                return "General Search"
            else:
                return "General Search"

        # 3️⃣ Combined domain + path tokens (non-search engines)
        parsed = urlparse(url)
        combined = " ".join(filter(None, [dom_clean, parsed.path.replace("/", " "), parsed.query])).lower()
        if re.search(Sessionization.KW_EDU, combined):
            return "Education/Career"
        if re.search(Sessionization.KW_SOCIAL, combined):
            return "Social/Entertainment"
        if re.search(Sessionization.KW_SHOP, combined):
            return "Shopping"
        if re.search(Sessionization.KW_FIN, combined):
            return "Finance"
        if re.search(Sessionization.KW_TRAVEL, combined):
            return "Travel"

        # 4️⃣ Heuristics for generic domain names
        sld = dom_clean.split(".")[-2] if len(dom_clean.split(".")) >= 2 else dom_clean
        if sld in ("blog", "news", "press", "media"):
            return "Social/Entertainment"
        if sld in ("shop", "store", "deal", "promo"):
            return "Shopping"

        # 5️⃣ Default fallback
        return "Miscellaneous"

    # -----------------------------------------
    # Sessionization Logic
    # -----------------------------------------
    @staticmethod
    def sessionization(df):
        """Group browsing data into 1-hour sessions and aggregate stats."""
        # 1️⃣ Assign hourly sessions
        df['session_start_hour'] = df['visit_time'].dt.floor('H')
        df['session_id'] = df['user'] + "_hour_" + df['session_start_hour'].dt.strftime('%Y%m%d%H')

        # 2️⃣ Categorize each URL
        df['category'] = df['url'].apply(Sessionization.categorize_domain_from_url)
        df['domain'] = df['url'].apply(Sessionization.normalize_domain)

        # 3️⃣ Aggregate by session
        session_summary = (
            df.groupby(['user', 'session_id'])
            .agg(
                session_start=('visit_time', 'min'),
                session_end=('visit_time', 'max'),
                num_visits=('url', 'count'),
                unique_domains=('domain', 'nunique'),
                domains_list=('domain', lambda x: list(x.dropna().unique())),
                categories_list=('category', lambda x: list(x))
            )
            .reset_index()
        )

        # 4️⃣ Compute durations
        session_summary['observed_span'] = session_summary['session_end'] - session_summary['session_start']
        session_summary['session_duration'] = pd.Timedelta(hours=1)
        session_summary['duration_minutes_observed'] = session_summary['observed_span'].dt.total_seconds() / 60
        session_summary['duration_minutes'] = 60

        # 5️⃣ Dominant category
        session_summary['dominant_category'] = session_summary['categories_list'].apply(
            lambda cat_list: Counter(cat_list).most_common(1)[0][0] if cat_list else "Miscellaneous"
        )

        # 6️⃣ Category proportions
        def category_proportions(cat_list):
            c = Counter(cat_list)
            total = sum(c.values())
            if total == 0:
                return {}
            return {k: v / total for k, v in c.items()}

        cat_props = session_summary['categories_list'].apply(category_proportions)
        cat_props_df = pd.json_normalize(cat_props).fillna(0)

        # 7️⃣ Merge and return
        session_df = pd.concat([session_summary, cat_props_df], axis=1)
        print("✅ Sessionization complete. Columns:", session_df.columns.tolist())
        return session_df

# sessions = Sessionization()
# df = DataCollection.final_data()
# print(sessions.sessionization(df))