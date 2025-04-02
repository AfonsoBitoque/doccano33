<template>
    <v-main>
      <admin-dashboard />
    </v-main>
  </template>
  
  <script>
  import AdminDashboard from '@/components/admin/AdminDashboard'
  
  export default {
    components: {
      AdminDashboard
    },
    
    layout: 'default',
    
    middleware: ['check-auth', 'admin-only']
  }
  </script>