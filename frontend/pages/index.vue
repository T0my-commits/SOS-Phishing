<template>
  <div>
    <h2>Welcome to my app</h2>

    <div class="container">
      <div class="centered-element">
        <p>No campaign started</p>
        <div class="p-button p-component">
          <NuxtLink class="p-button-label" to="/new-test-campaign">Create a new one</NuxtLink>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
}

.p-button a {
    color: white;
    text-decoration: none;
}
.p-button a:hover, 
.p-button a:focus {
    color: #ffffff;
}
</style>
