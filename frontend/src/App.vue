<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-title class="font-weight-bold">
        <v-icon left>mdi-handshake</v-icon>
        Group By Sharing
      </v-app-bar-title>

      <v-spacer />

      <v-btn to="/" variant="text">
        <v-icon>mdi-home</v-icon>
        Home
      </v-btn>

      <v-btn to="/products" variant="text">
        <v-icon>mdi-package-variant</v-icon>
        Products
      </v-btn>

      <v-btn to="/pools" variant="text">
        <v-icon>mdi-account-group</v-icon>
        Pools
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
//
</script>
