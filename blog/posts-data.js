// Newest post first. Each new_blog_post.py run prepends one entry here.
const BLOG_POSTS = [
  {
    slug: "healing-childhood-wounds-and-trauma-a-path-to-wholeness",
    image: "images/healing-childhood-wounds.jpeg",
    title: "Healing Childhood Wounds and Trauma: A Path to Wholeness",
    excerpt: "Childhood wounds shape us, but they don't have to define us. A gentle, evidence-based guide to healing your inner child and reclaiming wholeness.",
    date: "2026-07-18",
    readTime: "4 min read",
    category: "Mental Health"
  },
  {
    slug: "7-factors-that-worsen-mental-health-as-you-age-and-gentle-ways-to-protect-it",
    title: "7 Factors That Worsen Mental Health As You Age (And Gentle Ways to Protect It)",
    excerpt: "Understanding the common factors behind mental health decline as you age, plus gentle, realistic ways to protect your peace.",
    date: "2026-07-17",
    readTime: "3 min read",
    category: "Mental Health",
    image: "images/mental-health-aging.jpeg"
  },
  {
    slug: "am-i-anxious-or-just-stressed-understanding-the-difference-and-how-to-find-your-calm",
    title: "Am I Anxious or Just Stressed? Understanding the Difference and How to Find Your Calm",
    excerpt: "How to tell stress and anxiety apart, the symptoms of each, self-reflection questions, and gentle ways to find your calm.",
    date: "2026-07-17",
    readTime: "4 min read",
    category: "Wellness",
    image: "images/anxious-or-just-stressed.png"
  },
  {
    slug: "home-pilates-for-men-and-women-complete-beginner-guide",
    title: "Home Pilates for Men and Women: Complete Beginner Guide",
    excerpt: "A complete beginner guide to building core strength, posture, and flexibility with a simple 20-minute home Pilates routine for men and women.",
    date: "2026-07-16",
    readTime: "3 min read",
    category: "Fitness",
    image: "images/home-pilates.jpeg"
  },
  {
    slug: "easy-one-pan-keto-chicken-and-vegetables-low-carb-20-minutes",
    title: "Easy One-Pan Keto Chicken and Vegetables (Low Carb, 20 Minutes)",
    excerpt: "A 20-minute, one-pan keto chicken and vegetable dinner that is high in protein, low in carbs, and easy to meal prep.",
    date: "2026-07-14",
    readTime: "2 min read",
    category: "Wellness Recipes",
    image: "images/keto-chicken-veggies.jpeg"
  },
  {
    slug: "morning-glow-magic-detox-tea-lemon-and-lime-recipe-for-glowing-skin-and-energy",
    title: "Morning Glow Magic Detox Tea: Lemon and Lime Recipe for Glowing Skin and Energy",
    excerpt: "A caffeine-light citrus detox tea with ginger, turmeric, and hibiscus for glowing skin, gut health, and natural morning energy.",
    date: "2026-07-13",
    readTime: "2 min read",
    category: "Wellness Recipes",
    image: "images/morning-glow-detox-tea.jpeg"
  },
  {
    slug: "the-ritual-reclaiming-joy-after-burnout",
    title: "The Ritual: Reclaiming Joy After Burnout",
    excerpt: "A gentle 40-minute evening wind-down ritual, stretching, chamomile tea, and gratitude, to release workday tension and reclaim your rest.",
    date: "2026-07-11",
    readTime: "2 min read",
    category: "Wellness",
    image: "images/evening-wind-down-ritual.jpeg"
  },
  {
    slug: "reclaiming-joy-after-burnout-a-gentle-guide-to-feeling-like-yourself-again",
    title: "Reclaiming Joy After Burnout: A Gentle Guide to Feeling Like Yourself Again",
    excerpt: "Burnout quietly steals your joy, here is how to slowly rebuild rest, pleasure, and meaning without forcing it.",
    date: "2026-07-10",
    readTime: "6 min read",
    category: "Wellness",
    image: "images/reclaiming-joy-after-burnout.png"
  },
  {
    slug: "how-to-build-unshakable-confidence-one-kept-promise-at-a-time",
    title: "How to Build Unshakable Confidence (One Kept Promise at a Time)",
    excerpt: "Confidence is not something you are born with. It is built quietly, in private, one small kept promise at a time. Here is how to begin.",
    date: "2026-07-09",
    readTime: "5 min read",
    category: "Confidence",
    image: "images/unshakable-confidence.jpg"
  },
  {
    slug: "why-putting-yourself-last-feels-normal-but-is-quietly-destroying-your-glow",
    title: "Why Putting Yourself Last Feels Normal (But Is Quietly Destroying Your Glow)",
    excerpt: "Choosing everyone else first feels like the default setting. Here are 5 gentle ways to start choosing you, without the guilt.",
    date: "2026-07-08",
    readTime: "4 min read",
    category: "Self-Care",
    image: "images/putting-yourself-last.png"
  },
  {
    slug: "nutrition-without-the-guilt-how-to-eat-in-your-glow-era",
    title: "Nutrition Without the Guilt: How to Eat in Your Glow Era",
    excerpt: "Diet culture taught you to fear food. Here's a gentler, more sustainable way to nourish your body and actually feel good.",
    date: "2026-07-07",
    readTime: "3 min read",
    category: "Wellness",
    image: "images/nutrition.jpeg"
  },
  {
    slug: "the-silent-killer-how-lack-of-sleep-raises-your-risk-of-stroke",
    title: "The Silent Killer: How Lack of Sleep Raises Your Risk of Stroke",
    excerpt: "How chronic sleep loss quietly raises your risk of stroke, heart disease, and more, plus practical tips to sleep better tonight.",
    date: "2026-07-06",
    readTime: "3 min read",
    category: "Wellness",
    image: "images/glow-arrow-one.png"
  },
  {
    slug: "why-your-self-care-routine-keeps-failing",
    title: "Why Your Self-Care Routine Keeps Failing (And What Actually Works)",
    excerpt: "Most self-care advice is built for a life you don't have. Here's the gentler, more honest approach Glow Era teaches instead.",
    date: "2026-07-06",
    readTime: "5 min read",
    category: "Self-Care"
  },
  {
    slug: "the-boundary-you-are-most-afraid-to-set",
    title: "The Boundary You're Most Afraid to Set (And Why It Will Set You Free)",
    excerpt: "Boundaries aren't walls. They're the quiet, powerful act of telling the truth about what you need.",
    date: "2026-07-05",
    readTime: "4 min read",
    category: "Boundaries"
  },
  {
    slug: "how-to-start-your-glow-era-today",
    title: "How to Start Your Glow Era Today (Even If You Don't Feel Ready)",
    excerpt: "You don't need a clean slate, a new year, or perfect timing. You just need to begin. Here's how.",
    date: "2026-07-04",
    readTime: "4 min read",
    category: "Confidence"
  }
];
