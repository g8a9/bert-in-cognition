<script>
  import svelteLogo from './assets/svelte.svg'

  let words = "dog, cat, man, uomo";
  let layer = 11;
  let averaged = true;

  let promise;

  function handleClick() {
    promise = getSimilarities();
  }

  async function getSimilarities() {
    const location = "127.0.0.1";

    const body = {
      words: words.split(",").map((w) => w.trim()),
      layer: layer,
      aggregation: averaged ? "average" : "non-contextualised"
    };
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            // 'Access-Control-Allow-Origin': "*",
            // 'Access-Control-Allow-Methods': 'GET, POST'
        },
        body: JSON.stringify(body)
    };

    try {
        const fetchResponse = await fetch(`http://${location}:8000/prototypes`, settings);
        const data = await fetchResponse.json();
        console.log(data);
        console.log(data.similarities);

        return data;
    } catch (e) {
        return e;
    }
}

</script>

<main>
  <div>
    
    <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    
  </div>
  <h1>Bert In Cognition</h1>

  <p>
    Compute pairwise similarity between words (prototypes or non-contextualised).
  </p>
  <p class="read-the-docs">
    Insert: words (separated by a comma), BERT's layer, check if averaged.
  </p>

  <input type=text id=words bind:value={words}>
  <input type=number id=layer bind:value={layer} min=0 max=11>
  <input type=checkbox bind:checked={averaged}>
  
  <button on:click={handleClick}>Compute</button>

  {#if promise != undefined}
    {#await promise}
      <p>Computing Similarities...</p>
    {:then response}
      <p>Cosine Similarities</p>
      <ul>
        {#each response.similarities as s}
          <li>
            {s.w1}, {s.w2}, {s.sim}
          </li>
        {/each}
      </ul>

      <p>Words we don't have in the vocabulary</p>
      <ul>
        {#each response.oov_words as w}
          <li>
            {w}
          </li>
        {/each}
      </ul>

    {/await}  
  {/if}

</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
