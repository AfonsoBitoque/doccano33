<template>
  <v-card class="elevation-0">
    <v-card-title>
      <v-list-item class="grow ps-0">
        <v-list-item-avatar>
          <v-icon large>
            {{ mdiAccountCircle }}
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>{{ perspective.username }}</v-list-item-title>
          <v-list-item-subtitle>
            {{
              perspective.createdAt 
                | dateParse('YYYY-MM-DDTHH:mm:ss') 
                | dateFormat('DD/MM/YYYY HH:mm')
            }}
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-row align="center" justify="end">
          <v-menu v-if="perspective.user == userId" bottom left>
            <template #activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>{{ mdiDotsVertical }}</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-item>
                <v-list-item-title @click="showEdit = true"> Edit </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title @click="$emit('delete-perspective', perspective)">
                  Delete
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-row>
      </v-list-item>
    </v-card-title>

    <v-card-text class="body-1">
      <span v-if="!showEdit">
        {{ perspective.text }}
      </span>
      <v-form v-else v-model="valid">
        <v-row>
          <v-textarea v-model="editText" auto-grow rows="1" solo :rules="perspectiveRules" />
        </v-row>
        <v-row justify="end">
          <v-btn text class="text-capitalize" @click="cancel"> Cancel </v-btn>
          <v-btn
            :disabled="!valid"
            color="primary"
            class="text-capitalize"
            @click="updatePerspective(editText)"
          >
            update
          </v-btn>
        </v-row>
      </v-form>
    </v-card-text>
    <v-divider />
  </v-card>
</template>

<script lang="ts">
import { mdiAccountCircle, mdiDotsVertical } from '@mdi/js'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
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

Vue.use(VueFilterDateFormat)
Vue.use(VueFilterDateParse)

export default Vue.extend({
  props: {
    perspective: {
      required: true,
      type: Object as PropType<PerspectiveItem>
    },
    userId: {
      required: true,
      type: Number
    }
  },

  data() {
    return {
      showEdit: false,
      editText: this.perspective.text,
      perspectiveRules: [(v: string) => !!v.trim() || 'Perspectiva é obrigatória'],
      valid: false,
      mdiAccountCircle,
      mdiDotsVertical
    }
  },

  methods: {
    cancel() {
      this.showEdit = false
      this.editText = this.perspective.text
    },

    updatePerspective(text: string) {
      this.$emit('update-perspective', { ...this.perspective, text })
      this.showEdit = false
    }
  }
})
</script>