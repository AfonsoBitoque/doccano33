<template>
  <v-form v-model="valid">
    <v-textarea
      v-model="message"
      auto-grow
      hide-details
      outlined
      rows="1"
      name="PerspectiveInput"
      label="Write your perspective"
      :rules="perspectiveRules"
    />
    <v-btn
      class="white--text text-capitalize mt-3"
      color="primary"
      depressed
      :disabled="!valid"
      @click="addPerspective"
    >
      Send
    </v-btn>
  </v-form>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      perspectiveRules: [(v: string) => !!v.trim() || 'Perspectiva é obrigatória'],
      message: '',
      valid: false
    }
  },

  methods: {
    addPerspective() {
      this.$emit('add-perspective', this.message)
      this.message = ''
    }
  }
})
</script>