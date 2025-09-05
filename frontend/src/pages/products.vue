<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Products Management</span>
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon left>mdi-plus</v-icon>
              Add Product
            </v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Products List</v-card-title>
          <v-card-text>
            <v-data-table
              class="elevation-1"
              :headers="headers"
              :items="products"
              :loading="loading"
            >
              <template #item.unit_price="{ item }">
                ${{ item.unit_price.toFixed(2) }}
              </template>

              <template #item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>

              <template #item.actions="{ item }">
                <v-btn
                  class="mr-2"
                  icon="mdi-pencil"
                  size="small"
                  @click="openEditDialog(item)"
                />
                <v-btn
                  color="error"
                  icon="mdi-delete"
                  size="small"
                  @click="deleteProduct(item.id)"
                />
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? "Edit" : "Create" }} Product</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="form.name"
              label="Product Name"
              required
              :rules="[(v) => !!v || 'Name is required']"
            />

            <v-textarea
              v-model="form.description"
              label="Description"
              rows="3"
            />

            <v-text-field
              v-model="form.unit_price"
              label="Unit Price"
              min="0"
              required
              :rules="[
                (v) => !!v || 'Price is required',
                (v) => v > 0 || 'Price must be greater than 0',
              ]"
              step="0.01"
              type="number"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!valid || saving"
            :loading="saving"
            variant="text"
            @click="saveProduct"
          >
            {{ isEditing ? "Update" : "Create" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete this product? This action cannot be
          undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            variant="text"
            @click="confirmDelete"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
  import { onMounted, ref } from 'vue'
  import { type Product, productApi } from '@/services/api'

  const products = ref<Product[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)
  const dialog = ref(false)
  const deleteDialog = ref(false)
  const valid = ref(false)
  const isEditing = ref(false)
  const form = ref({
    name: '',
    description: '',
    unit_price: '',
  })
  const productToDelete = ref<number | null>(null)
  const editingProductId = ref<number | null>(null)

  const headers = [
    { title: 'ID', key: 'id', sortable: true },
    { title: 'Name', key: 'name', sortable: true },
    { title: 'Description', key: 'description', sortable: false },
    { title: 'Unit Price', key: 'unit_price', sortable: true },
    { title: 'Created', key: 'created_at', sortable: true },
    { title: 'Actions', key: 'actions', sortable: false },
  ]

  async function loadProducts () {
    loading.value = true
    try {
      const response = await productApi.getAll()
      products.value = response.data
    } catch (error) {
      console.error('Error loading products:', error)
    // You could add a snackbar here to show error message
    } finally {
      loading.value = false
    }
  }

  function openCreateDialog () {
    isEditing.value = false
    editingProductId.value = null
    form.value = {
      name: '',
      description: '',
      unit_price: '',
    }
    dialog.value = true
  }

  function openEditDialog (product: Product) {
    isEditing.value = true
    editingProductId.value = product.id
    form.value = {
      name: product.name,
      description: product.description,
      unit_price: product.unit_price.toString(),
    }
    dialog.value = true
  }

  function closeDialog () {
    dialog.value = false
    editingProductId.value = null
    form.value = {
      name: '',
      description: '',
      unit_price: '',
    }
  }

  async function saveProduct () {
    // Don't submit if form is not valid
    if (!valid.value) {
      console.log('Form validation failed, not submitting')
      return
    }

    saving.value = true
    try {
      const productData = {
        name: form.value.name,
        description: form.value.description,
        unit_price: Number.parseFloat(form.value.unit_price), // Convert to number for decimal field
      }
      console.log('Sending product data:', productData)

      await (isEditing.value && editingProductId.value ? productApi.update(editingProductId.value, productData) : productApi.create(productData))

      await loadProducts()
      closeDialog()
    } catch (error: any) {
      console.error('Error saving product:', error)
      console.error('Error details:', error.response?.data)
    // You could add a snackbar here to show error message
    } finally {
      saving.value = false
    }
  }

  function deleteProduct (id: number) {
    productToDelete.value = id
    deleteDialog.value = true
  }

  async function confirmDelete () {
    if (!productToDelete.value) return

    deleting.value = true
    try {
      await productApi.delete(productToDelete.value)
      await loadProducts()
      deleteDialog.value = false
      productToDelete.value = null
    } catch (error) {
      console.error('Error deleting product:', error)
    // You could add a snackbar here to show error message
    } finally {
      deleting.value = false
    }
  }

  function formatDate (dateString: string) {
    return new Date(dateString).toLocaleDateString()
  }

  onMounted(() => {
    loadProducts()
  })
</script>
