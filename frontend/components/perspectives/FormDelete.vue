<template>
  <v-card>
    <v-card-title class="headline">Excluir perspectivas</v-card-title>
    <v-card-text>
      Tem certeza que deseja excluir {{ selected.length }} perspectiva(s)?
      <v-alert type="warning" class="mb-0 mt-4">
        Esta ação não pode ser desfeita.
      </v-alert>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="$emit('cancel')">Cancelar</v-btn>
      <v-btn color="error" text @click="$emit('remove')">Excluir</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'

// Definindo a interface para o item de perspectiva
interface PerspectiveItem {
  id: number
  user: number
  username: string
  text: string
  createdAt: string
  updatedAt: string
}

export default Vue.extend({
  props: {
    selected: {
      type: Array as PropType<PerspectiveItem[]>,
      default: () => [],
      required: true
    }
  }
})
</script>