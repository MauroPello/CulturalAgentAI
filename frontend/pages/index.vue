<template>
  <div class="space-y-16 md:space-y-24">
    <!-- Hero Section -->
    <UContainer class="py-16 md:py-24 text-center">
      <div class="flex flex-row justify-center gap-4 mb-4 w-full">
        <UButton color="white" size="sm" to="/#find-meal"
          >🔄 Surprise Me!</UButton
        >
        <UButton color="white" size="sm" to="/all-recipes"
          >🍝 Show Me Recipes</UButton
        >
      </div>
      <h1
        class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-4"
      >
        Tired of the Same Old Meals?
      </h1>
      <p
        class="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8"
      >
        Stop staring blankly at the fridge. Let us spark your culinary
        creativity by suggesting ingredients and matching recipes you'll love.
        Break free from your cooking rut today!
      </p>
      <div class="flex flex-col sm:flex-row justify-center items-center gap-4">
        <UButton
          size="xl"
          icon="i-heroicons-sparkles-20-solid"
          label="Get Inspired Now!"
          aria-label="Start finding an ingredient"
          trailing
          to="/#find-meal"
        />
        <UButton
          to="/all-recipes"
          size="xl"
          label="Browse All Recipes"
          variant="link"
          color="gray"
          icon="i-heroicons-book-open"
          trailing
        />
      </div>
    </UContainer>

    <!-- How it Works Section -->
    <UContainer>
      <div class="max-w-4xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-12">
          How It Works: Simple as 1-2-3
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-sparkles-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">1. Get Inspired</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Start with a randomly suggested ingredient. Like it? Keep it!
              Don't like it? Get another one instantly.
            </p>
          </div>
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-plus-circle-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">2. Add More</h3>
            <p class="text-gray-600 dark:text-gray-300">
              We'll suggest compatible ingredients that work well with your
              choices. Accept or reject them until you're happy.
            </p>
          </div>
          <div class="text-center space-y-3 p-4 rounded-lg">
            <div
              class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 rounded-full mb-4 ring-8 ring-primary-50 dark:ring-primary-950"
            >
              <UIcon name="i-heroicons-document-text-solid" class="w-8 h-8" />
            </div>
            <h3 class="text-xl font-semibold">3. Find Recipes</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Based on your final ingredients, we'll find matching recipes and
              show you exactly what else you need to make the dish.
            </p>
          </div>
        </div>
      </div>
    </UContainer>

    <!-- Feature/Benefit Section -->
    <UContainer class="py-16">
      <div class="grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h2 class="text-3xl md:text-4xl font-bold mb-4">
            Never Ask "What Should I Cook?" Again
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Our unique ingredient-first approach helps you discover new
            combinations and rediscover the joy of cooking. Perfect for using up
            pantry items or simply finding fresh ideas.
          </p>
          <ul class="space-y-3 text-gray-700 dark:text-gray-200">
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-check-circle-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span>Break free from boring meal routines.</span>
            </li>
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-check-circle-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span>Discover recipes based on ingredients you like.</span>
            </li>
            <li class="flex items-center gap-3">
              <UIcon
                name="i-heroicons-check-circle-solid"
                class="w-6 h-6 text-primary-500"
              />
              <span>Simple, intuitive, and fun to use.</span>
            </li>
          </ul>
          <UButton
            size="lg"
            label="Let's Find Your Next Meal!"
            class="mt-8"
            icon="i-heroicons-arrow-right-20-solid"
            trailing
            to="/#find-meal"
          />
        </div>
        <div v-if="isMinimumSm" class="w-full md:px-2 lg:px-6 xl:px-8">
          <RecipePreview
            :recipe="recipe"
            :is-accepted="false"
            :selected-ingredients="[]"
            :current-recipe-acceptance-count="0"
            :hide-likes-and-dislikes="true"
          />
        </div>
      </div>
    </UContainer>

    <!-- Final Call to Action -->
    <UContainer id="find-meal" class="pb-16 text-center">
      <h2 class="text-3xl md:text-4xl font-bold mb-4">
        Ready to Get Inspired?
      </h2>
      <p class="text-lg text-gray-600 dark:text-gray-300 max-w-xl mx-auto mb-8">
        Click the button below to start your journey towards more exciting and
        delicious home-cooked meals. It's free and easy!
      </p>
      <StartGame />
    </UContainer>

    <UContainer class="pb-16 text-center">
      <UIcon name="i-heroicons-gift" class="text-4xl text-primary mb-3" />
      <h2
        class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white mb-2"
      >
        Do you enjoy using the App? Offer me a coffee!
      </h2>
      <p
        class="text-lg text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto"
      >
        Your support helps keep this app running, improving, and reaching more
        people who love cooking and exploring new recipes. Every contribution,
        no matter how small, makes a significant difference in maintaining and
        enhancing the features you enjoy. We appreciate your generosity and
        thank you for being part of our journey to make cooking more enjoyable
        for everyone!
      </p>
      <UButton
        icon="i-heroicons-banknotes"
        size="xl"
        to="https://www.paypal.com/donate/?hosted_button_id=8A7748MA4QM76"
        target="_blank"
        rel="noopener noreferrer"
        variant="soft"
        color="primary"
      >
        Buy Me a Coffee
      </UButton>
    </UContainer>
  </div>
</template>

<script lang="ts" setup>
const recipe = {
  id: "52768",
  name: "Apple Frangipan Tart",
  category: "Dessert",
  area: "English",
  instructions:
    "Preheat the oven to 200C/180C Fan/Gas 6.\r\nPut the biscuits in a large re-sealable freezer bag and bash with a rolling pin into fine crumbs. Melt the butter in a small pan, then add the biscuit crumbs and stir until coated with butter. Tip into the tart tin and, using the back of a spoon, press over the base and sides of the tin to give an even layer. Chill in the fridge while you make the filling.\r\nCream together the butter and sugar until light and fluffy. You can do this in a food processor if you have one. Process for 2-3 minutes. Mix in the eggs, then add the Almonds and almond extract and blend until well combined.\r\nPeel the apples, and cut thin slices of apple. Do this at the last minute to prevent the apple going brown. Arrange the slices over the biscuit base. Spread the frangipane filling evenly on top. Level the surface and sprinkle with the flaked almonds.\r\nBake for 20-25 minutes until golden-brown and set.\r\nRemove from the oven and leave to cool for 15 minutes. Remove the sides of the tin. An easy way to do this is to stand the tin on a can of beans and push down gently on the edges of the tin.\r\nTransfer the tart, with the tin base attached, to a serving plate. Serve warm with cream, crème fraiche or ice cream.",
  tags: ["Tart", "Baking", "Fruity"],
  youtubeUrl: "https://www.youtube.com/watch?v=rp8Slv4INLk",
  ingredients: [
    {
      ingredient: "Digestive Biscuits",
      measure: "175g/6oz",
    },
    {
      ingredient: "Butter",
      measure: "75g/3oz",
    },
    {
      ingredient: "Apples",
      measure: "200g/7oz",
    },
    {
      ingredient: "Sugar",
      measure: "75g/3oz",
    },
    {
      ingredient: "Eggs",
      measure: "2",
    },
    {
      ingredient: "Almonds",
      measure: "75g/3oz",
    },
    {
      ingredient: "Almond Extract",
      measure: "1 tsp",
    },
    {
      ingredient: "Flaked Almonds",
      measure: "50g/1¾oz",
    },
  ],
  slug: "apple-frangipan-tart",
};

const { isMinimumSm } = useScreenSize();
</script>
