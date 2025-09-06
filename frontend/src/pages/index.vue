<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4 text-center pa-8">
            Welcome to
            <span class="font-weight-bold text-primary">
              Group By Sharing
            </span>
          </v-card-title>
          <v-card-text class="text-center pa-8">
            <p class="text-h6 mb-4">
              Manage your products, create pools, and join group purchases!
            </p>
            <p class="text-body-1">Use the navigation above to get started.</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="4">
        <v-card class="h-100" hover>
          <v-card-title>
            <v-icon class="mr-2">mdi-package-variant</v-icon>
            Products
          </v-card-title>
          <v-card-text>
            Create and manage your product catalog. Add products with
            descriptions and pricing.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/products" variant="outlined">
              Manage Products
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="h-100" hover>
          <v-card-title>
            <v-icon class="mr-2">mdi-account-group</v-icon>
            Pools
          </v-card-title>
          <v-card-text>
            Create group purchase pools for your products. Set minimum
            quantities and timeframes.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/pools" variant="outlined">
              Manage Pools
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="h-100" hover>
          <v-card-title>
            <v-icon class="mr-2">mdi-account-plus</v-icon>
            Join Pools
          </v-card-title>
          <v-card-text>
            Browse available pools and join group purchases by entering your
            email and desired quantity.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" to="/pools" variant="outlined">
              Browse Pools
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
//
</script>
