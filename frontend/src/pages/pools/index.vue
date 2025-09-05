<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <span>Pools Management</span>
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon left>mdi-plus</v-icon>
              Add Pool
            </v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Pools List</v-card-title>
          <v-card-text>
            <v-data-table
              class="elevation-1"
              :headers="headers"
              :items="poolsWithProducts"
              :loading="loading"
            >
              <template #item.product_name="{ item }">
                {{ getProductName(item.product) }}
              </template>

              <template #item.start_at="{ item }">
                {{ formatDate(item.start_at) }}
              </template>

              <template #item.end_at="{ item }">
                {{ formatDate(item.end_at) }}
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
                  @click="deletePool(item.id)"
                />
                <v-btn
                  class="ml-2"
                  color="success"
                  icon="mdi-account-plus"
                  size="small"
                  @click="openJoinDialog(item)"
                />
                <v-btn
                  class="ml-2"
                  color="info"
                  icon="mdi-format-list-bulleted"
                  size="small"
                  @click="viewRequests(item.id)"
                />
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Pool Dialog -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEditing ? 'Edit' : 'Create' }} Pool</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-select
              v-model="form.product"
              item-title="name"
              item-value="id"
              :items="products"
              label="Product"
              required
              :rules="[v => !!v || 'Product is required']"
            />

            <v-text-field
              v-model="form.start_at"
              label="Start Date & Time"
              required
              :rules="[v => !!v || 'Start date is required']"
              type="datetime-local"
            />

            <v-text-field
              v-model="form.end_at"
              label="End Date & Time"
              required
              :rules="[v => !!v || 'End date is required']"
              type="datetime-local"
            />

            <v-text-field
              v-model="form.min_quantity"
              label="Minimum Quantity"
              min="1"
              required
              :rules="[v => !!v || 'Minimum quantity is required', v => v > 0 || 'Minimum quantity must be greater than 0']"
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
            @click="savePool"
          >
            {{ isEditing ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Join Pool Dialog -->
    <v-dialog v-model="joinDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Join Pool</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="joinForm" v-model="joinValid">
            <v-text-field
              v-model="joinForm.email"
              label="Email"
              required
              :rules="[v => !!v || 'Email is required', v => /.+@.+\..+/.test(v) || 'Email must be valid']"
              type="email"
            />

            <v-text-field
              v-model="joinForm.quantity"
              label="Quantity"
              min="1"
              required
              :rules="[v => !!v || 'Quantity is required', v => v > 0 || 'Quantity must be greater than 0']"
              type="number"
            />
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeJoinDialog">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :disabled="!joinValid || joining"
            :loading="joining"
            variant="text"
            @click="joinPool"
          >
            Join Pool
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>
          Are you sure you want to delete this pool? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="error" :loading="deleting" variant="text" @click="confirmDelete">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
  import { computed, onMounted, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { type Pool, poolApi, type Product, productApi, requestApi } from '@/services/api'

  const router = useRouter()
  const pools = ref<Pool[]>([])
  const products = ref<Product[]>([])
  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)
  const joining = ref(false)
  const dialog = ref(false)
  const joinDialog = ref(false)
  const deleteDialog = ref(false)
  const valid = ref(false)
  const joinValid = ref(false)
  const isEditing = ref(false)
  const form = ref({
    product: null as number | null,
    start_at: '',
    end_at: '',
    min_quantity: 1,
  })
  const joinForm = ref({
    email: '',
    quantity: 1,
  })
  const poolToDelete = ref<number | null>(null)
  const selectedPool = ref<Pool | null>(null)
  const editingPoolId = ref<number | null>(null)

  const headers = [
    { title: 'ID', key: 'id', sortable: true },
    { title: 'Product', key: 'product_name', sortable: true },
    { title: 'Start Date', key: 'start_at', sortable: true },
    { title: 'End Date', key: 'end_at', sortable: true },
    { title: 'Min Quantity', key: 'min_quantity', sortable: true },
    { title: 'Created', key: 'created_at', sortable: true },
    { title: 'Actions', key: 'actions', sortable: false },
  ]

  const poolsWithProducts = computed(() => {
    return pools.value.map(pool => ({
      ...pool,
      product_name: getProductName(pool.product),
    }))
  })

  async function loadPools () {
    loading.value = true
    try {
      const response = await poolApi.getAll()
      pools.value = response.data
    } catch (error) {
      console.error('Error loading pools:', error)
    } finally {
      loading.value = false
    }
  }

  async function loadProducts () {
    try {
      const response = await productApi.getAll()
      products.value = response.data
    } catch (error) {
      console.error('Error loading products:', error)
    }
  }

  function getProductName (productId: number) {
    const product = products.value.find(p => p.id === productId)
    return product ? product.name : `Product ${productId}`
  }

  function openCreateDialog () {
    isEditing.value = false
    editingPoolId.value = null
    form.value = {
      product: null,
      start_at: '',
      end_at: '',
      min_quantity: 1,
    }
    dialog.value = true
  }

  function openEditDialog (pool: Pool) {
    isEditing.value = true
    editingPoolId.value = pool.id
    form.value = {
      product: pool.product,
      start_at: formatDateTimeForInput(pool.start_at),
      end_at: formatDateTimeForInput(pool.end_at),
      min_quantity: pool.min_quantity,
    }
    dialog.value = true
  }

  function openJoinDialog (pool: Pool) {
    selectedPool.value = pool
    joinForm.value = {
      email: '',
      quantity: 1,
    }
    joinDialog.value = true
  }

  function closeDialog () {
    dialog.value = false
    editingPoolId.value = null
    form.value = {
      product: null,
      start_at: '',
      end_at: '',
      min_quantity: 1,
    }
  }

  function closeJoinDialog () {
    joinDialog.value = false
    joinForm.value = {
      email: '',
      quantity: 1,
    }
    selectedPool.value = null
  }

  async function savePool () {
    // Don't submit if form is not valid
    if (!valid.value) {
      console.log('Form validation failed, not submitting')
      return
    }

    saving.value = true
    try {
      const poolData = {
        product: form.value.product!,
        start_at: form.value.start_at,
        end_at: form.value.end_at,
        min_quantity: Number.parseInt(form.value.min_quantity.toString()), // Ensure it's an integer
      }
      console.log('Sending pool data:', poolData)

      await (isEditing.value && editingPoolId.value ? poolApi.update(editingPoolId.value, poolData) : poolApi.create(poolData))

      await loadPools()
      closeDialog()
    } catch (error: any) {
      console.error('Error saving pool:', error)
      console.error('Error details:', error.response?.data)
    } finally {
      saving.value = false
    }
  }

  async function joinPool () {
    if (!selectedPool.value) return

    // Don't submit if form is not valid
    if (!joinValid.value) {
      console.log('Join form validation failed, not submitting')
      return
    }

    joining.value = true
    try {
      await requestApi.create(selectedPool.value.id, {
        email: joinForm.value.email,
        quantity: Number.parseInt(joinForm.value.quantity.toString()), // Ensure it's an integer
      })
      closeJoinDialog()
    // You could add a success message here
    } catch (error: any) {
      console.error('Error joining pool:', error)
      console.error('Error details:', error.response?.data)

      // Handle specific error cases
      if (error.response?.status === 400 && error.response?.data?.email) {
        // Show user-friendly error message for duplicate email
        alert(`Error: ${error.response.data.email}`)
      } else {
        // Generic error message
        alert('Error joining pool. Please try again.')
      }
    } finally {
      joining.value = false
    }
  }

  function deletePool (id: number) {
    poolToDelete.value = id
    deleteDialog.value = true
  }

  function viewRequests (poolId: number) {
    router.push(`/pools/${poolId}/requests`)
  }

  async function confirmDelete () {
    if (!poolToDelete.value) return

    deleting.value = true
    try {
      await poolApi.delete(poolToDelete.value)
      await loadPools()
      deleteDialog.value = false
      poolToDelete.value = null
    } catch (error) {
      console.error('Error deleting pool:', error)
    } finally {
      deleting.value = false
    }
  }

  function formatDate (dateString: string) {
    return new Date(dateString).toLocaleDateString()
  }

  function formatDateTimeForInput (dateString: string) {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${year}-${month}-${day}T${hours}:${minutes}`
  }

  onMounted(async () => {
    await Promise.all([loadPools(), loadProducts()])
  })
</script>
