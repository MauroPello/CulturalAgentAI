export const mediaFolder = "";

export const companyName = "The Ingredient Draw";
export const companyUrl = "https://ingredientdraw.pages.dev/";
export const companySEOTitle = `${companyName} - Find Your Next Meal Idea!`;
export const companySEODescription = `Tired of the same meals? ${companyName} helps you discover exciting new recipes! Pick ingredients you like, and get random meal suggestions to inspire your next cooking adventure and grocery list.`;
export const companyLogo = `${companyUrl}${mediaFolder}logo.png`;
export const companyR2BucketUrl = "https://pub-e219489cd0c8437e8eca65d80236741f.r2.dev/";
export const companyMainStructuredData = {
  title: companySEOTitle,
  meta: [
    { name: 'description', content: companySEODescription },
    { name: 'keywords', content: "meal suggestions, recipe ideas, what to cook, ingredient based recipes, random meal generator, cooking inspiration, food discovery, meal planning, grocery list ideas, dinner ideas, lunch ideas" },
    { property: 'og:title', content: companySEOTitle },
    { property: 'og:description', content: companySEODescription },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: companyUrl },
    { property: 'og:image', content: companyLogo },
    { property: 'og:image:width', content: '900' },
    { property: 'og:image:height', content: '900' },
    { property: 'og:locale', content: 'en_US' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: companySEOTitle },
    { name: 'twitter:description', content: companySEODescription },
    { name: 'twitter:image', content: companyLogo },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "@id": `${companyUrl}#webapp`, // Use #webapp instead of #website or #game
        "name": companySEOTitle,
        "description": companySEODescription, // Use the new description
        "url": companyUrl,
        "applicationCategory": "LifestyleApplication", // More fitting category
        "operatingSystem": "Web Browser",
        "browserRequirements": "Requires JavaScript",
        "inLanguage": "en-US", // Changed locale to en-US
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "USD" // Assuming USD, adjust if needed
        }
      }),
    }
  ]
};
