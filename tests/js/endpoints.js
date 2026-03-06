let url = "https://python-fridge-app.fly.dev/products";

async function generate_recipes(products) {
  const response = await fetch(url + "/recipes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(products)
  });

  return response;
}

let products = ["chicken breast", "tortillas", "avocado"];

let response = await generate_recipes(products);
let data = await response.json();

if (data.status_code == 200) {
  console.log("Recipes:", data.output);
} else {
  console.log(`Failed with error: ${data.output}`);
}
