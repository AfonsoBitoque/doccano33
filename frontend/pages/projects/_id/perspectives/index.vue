<template>
  <v-card>
    <v-card-title>
     
      <v-dialog v-model="dialogDelete">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-card-title>

    <v-card-text>
      <form-create @add-perspective="addPerspective" />
      
      <v-divider class="my-4"></v-divider>
      
      <div v-if="perspectives.length > 0">

        
        <perspective
          v-for="perspective in perspectives"
          :key="perspective.id"
          :perspective="perspective"
          :user-id="userId"
          @update-perspective="updatePerspective"
          @delete-perspective="deletePerspective"
        />
      </div>
      <div v-else class="text-center pa-5">
        <p>Nenhuma perspectiva compartilhada ainda. Seja o primeiro a compartilhar!</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import FormCreate from '@/components/perspectives/FormCreate.vue'
import FormDelete from '@/components/perspectives/FormDelete.vue'
import Perspective from '@/components/perspectives/Perspective.vue'

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
  components: {
    FormCreate,
    FormDelete,
    Perspective
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      dialogDelete: false,
      selected: [] as PerspectiveItem[],
      perspectives: [] as PerspectiveItem[],
      userId: 0,
      nextId: 1,
      headers: [
        { text: 'Mensagem', value: 'text' },
        { text: 'Autor', value: 'username' },
        { text: 'Data', value: 'createdAt' }
      ]
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    }
  },

  mounted() {
    // Como não estamos usando o backend, vamos obter o ID do usuário do store
    const user = this.$store.getters['auth/getUser']
    this.userId = user ? user.id : 0
    
    // Carregar perspectivas do localStorage
    this.loadPerspectives()
    
    // Adicionar listener para eventos de armazenamento
    window.addEventListener('storage', this.handleStorageChange)
  },

  created() {
    // Não usar window no created hook
  },

  beforeDestroy() {
    // Remover listener quando o componente for destruído
    window.removeEventListener('storage', this.handleStorageChange)
  },

  methods: {
    // Manipular mudanças no localStorage de outras abas/janelas
    handleStorageChange(event: StorageEvent) {
      const key = `perspectives_${this.projectId}`
      if (event.key === key) {
        // Atualizar perspectivas quando outras abas/janelas modificarem o localStorage
        this.perspectives = JSON.parse(event.newValue || '[]')
        if (this.perspectives.length > 0) {
          const maxId = Math.max(...this.perspectives.map(p => p.id))
          this.nextId = maxId + 1
        }
      }
    },

    loadPerspectives() {
      const key = `perspectives_${this.projectId}`
      const savedPerspectives = localStorage.getItem(key)
      if (savedPerspectives) {
        this.perspectives = JSON.parse(savedPerspectives)
        // Encontrar o próximo ID disponível
        if (this.perspectives.length > 0) {
          const maxId = Math.max(...this.perspectives.map(p => p.id))
          this.nextId = maxId + 1
        }
      }
    },
    
    savePerspectives() {
      const key = `perspectives_${this.projectId}`
      localStorage.setItem(key, JSON.stringify(this.perspectives))
    },
    
    addPerspective(text: string) {
      const userId = this.$store.getters['auth/getUserId']
      const username = this.$store.getters['auth/getUsername']
      this.userId = userId || 0
      if (!userId || !username) {
        console.error('Usuário não encontrado')
        return
      }
      const now = new Date().toISOString()
      const newPerspective: PerspectiveItem = {
        id: this.nextId++,
        user: userId,
        username,
        text,
        createdAt: now,
        updatedAt: now
      }
      
      // Adiciona a nova perspectiva no início do array
      this.perspectives.unshift(newPerspective)
      this.savePerspectives()
      
      // Forçar atualização da visualização
      this.$forceUpdate()
      console.log('Perspectiva adicionada:', newPerspective)
    },
    
    updatePerspective(updatedPerspective: PerspectiveItem) {
      const index = this.perspectives.findIndex(p => p.id === updatedPerspective.id)
      if (index !== -1) {
        updatedPerspective.updatedAt = new Date().toISOString()
        this.perspectives.splice(index, 1, updatedPerspective)
        this.savePerspectives()
      }
    },
    
    deletePerspective(perspective: PerspectiveItem) {
      const index = this.perspectives.findIndex(p => p.id === perspective.id)
      if (index !== -1) {
        this.perspectives.splice(index, 1)
        this.savePerspectives()
      }
    },
    
    remove() {
      this.selected.forEach(perspective => {
        const index = this.perspectives.findIndex(p => p.id === perspective.id)
        if (index !== -1) {
          this.perspectives.splice(index, 1)
        }
      })
      this.savePerspectives()
      this.dialogDelete = false
      this.selected = []
    }
  }
})
</script>