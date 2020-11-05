let randomized = Math.floor(Math.random()*10)
	let categories = ['night-sky','darkness','night','city-lights','kathmandu-night','new-york-night','london-night','eiffel-tower-night','night-bridge','fireworks-night']
	fetch(`https://api.unsplash.com/search/photos?page=1&query=${categories[randomized]}&client_id=DWe3Aq2S4cOfU7K_NsuagSQ_CEr1v-Ya89-7K3U5KVQ`).then((response) => response.json()).then((apple) => {let syau = apple.results[randomized].urls.regular;document.body.style.backgroundImage = `url(${syau})`;})

	photoCategories = ['funny','funny-dog','funny-cat','jokes','comedy','kathmandu','hello','namaste','greeting','thinking']
  fetch(`https://api.unsplash.com/search/photos?page=1&query=${photoCategories[randomized]}&client_id=DWe3Aq2S4cOfU7K_NsuagSQ_CEr1v-Ya89-7K3U5KVQ`)
  .then((response) => response.json())
  .then((apple) => {let syau = apple.results[randomized].urls.full;
    document.querySelector('#hello').setAttribute('src',syau)})