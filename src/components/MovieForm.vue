<template>
  <form id="movieForm" @submit.prevent="saveMovie">
    <div v-if="success || errors.length > 0">
      <ul v-if="success">
        <li>Successfully added movie</li>
      </ul>
      <ul v-else>
        <li v-for="error in errors[0]">{{ error }}</li>
      </ul>
    </div>
    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input type="text" name="title" class="form-control" />

      <label for="desc" class="form-label">Movie Description</label>
      <textarea name="desc" class="form-control"></textarea>

      <label for="poster" class="form-label">Movie Poster</label>
      <input type="file" name="poster" class="form-control" />
    </div>
    <button type="submit">Submit</button>
  </form>
</template>
<script setup>
import { ref, onMounted } from "vue";
let crsf_token = ref("");

let errors = ref([]);
let success = ref(false);

onMounted(() => {
  getCrsfToken();
});

let getCrsfToken = () => {
  fetch("/api/v1/csrf-token", {
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((resp) => resp.json())
    .then((data) => {
      crsf_token.value = data.csrf_token;
    });
};

let saveMovie = () => {
  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);
  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: { "X-CSRFToken": crsf_token.value },
  })
    .then((resp) => resp.json())
    .then((data) => {
      if (data.errors) {
        errors.value = [data.errors];
      } else {
        success.value = true;
      }
    })
    .catch((error) => {
      console.log("FAILED");
    });
  errors.value = [];
  success.value = false;
};
</script>
