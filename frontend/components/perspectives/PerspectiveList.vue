<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-options': [10, 50, 100],
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #[`item.createdAt`]="{ item }">
      <span>{{ 
        item.createdAt | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('DD/MM/YYYY HH:mm')
      }}</span>
    </template>
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format'
import VueFilterDateParse from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'

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
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<PerspectiveItem[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<PerspectiveItem[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      search: '',
      options: {} as DataOptions,
      headers: [
        { text: 'Texto', value: 'text', sortable: false },
        { text: 'Usuário', value: 'username', sortable: false },
        { text: 'Criado em', value: 'createdAt', sortable: false }
      ],
      mdiMagnify
    }
  },

  watch: {
    options: {
      handler() {
        this.updateQuery()
      },
      deep: true
    },
    search() {
      this.options.page = 1
      this.updateQuery()
    }
  },

  methods: {
    updateQuery() {
      const query = {
        path: this.$route.path,
        query: {
          q: this.search,
          page: this.options.page,
          limit: this.options.itemsPerPage
        }
      }
      this.$emit('update:query', query)
    }
  }
})
</script>