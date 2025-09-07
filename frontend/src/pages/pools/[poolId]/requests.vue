<template>
  <div>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="d-flex align-center">
              <v-btn
                class="mr-3"
                icon="mdi-arrow-left"
                variant="text"
                @click="goBack"
              />
              <span>Pool Requests Management</span>
            </div>
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon left>mdi-plus</v-icon>
              Add Request
            </v-btn>
          </v-card-title>
          <v-card-text>
            <p class="text-subtitle-1 mb-0">
              Manage requests for: <strong>{{ selectedPoolName }}</strong>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Requests List</v-card-title>
          <v-card-text>
            <v-data-table
              class="elevation-1"
              :headers="headers"
              :items="requests"
              :loading="loading"
            >
              <template #item.email="{ item }">
                {{ item.email }}
              </template>

              <template #item.quantity="{ item }">
                {{ item.quantity }}
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
                  @click="deleteRequest(item.id)"
                />
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Request Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{
            isEditing ? "Edit Request" : "New Request"
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="formEmail"
              label="Email"
              required
              :rules="emailRules"
              type="email"
            />
            <v-text-field
              v-model="formQuantity"
              label="Quantity"
              min="1"
              required
              :rules="quantityRules"
              type="number"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue darken-1" text @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn
            color="blue darken-1"
            :disabled="!valid || saving"
            :loading="saving"
            text
            @click="saveRequest"
          >
            {{ isEditing ? "Update" : "Create" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Delete Request</v-card-title>
        <v-card-text>
          Are you sure you want to delete this request? This action cannot be
          undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue darken-1" text @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { poolApi, productApi, type Request, requestApi } from "@/services/api";

const route = useRoute("/pools/[poolId]/requests");
const router = useRouter();

// Get pool ID from route params
const poolId = computed(() => {
  const id = route.params.poolId as string;
  const parsedId = Number.parseInt(id);
  if (isNaN(parsedId)) {
    console.error("Invalid pool ID:", id);
    return 0;
  }
  return parsedId;
});

// Reactive data
const requests = ref<Request[]>([]);
const loading = ref(false);
const dialog = ref(false);
const deleteDialog = ref(false);
const valid = ref(false);
const saving = ref(false);
const isEditing = ref(false);
const editingRequestId = ref<number | null>(null);
const requestToDelete = ref<number | null>(null);
const selectedPoolName = ref("");

// Form data
const formEmail = ref("");
const formQuantity = ref(1);

// Validation rules
const emailRules = [
  (v: string) => !!v || "Email is required",
  (v: string) => /.+@.+\..+/.test(v) || "Email must be valid",
];

const quantityRules = [
  (v: number) => !!v || "Quantity is required",
  (v: number) => v > 0 || "Quantity must be greater than 0",
];

// Table headers
const headers = [
  { title: "Email", key: "email" },
  { title: "Quantity", key: "quantity" },
  { title: "Created At", key: "created_at" },
  { title: "Actions", key: "actions", sortable: false },
];

// Methods
async function loadRequests() {
  loading.value = true;
  try {
    const response = await requestApi.getByPool(poolId.value);
    requests.value = response.data;
  } catch (error) {
    console.error("Error loading requests:", error);
    alert("Error loading requests. Please try again.");
  } finally {
    loading.value = false;
  }
}

async function loadPoolName() {
  try {
    // Get the pool name from the pools API
    const poolsResponse = await poolApi.getAll();
    const pools = poolsResponse.data;
    const pool = pools.find((p) => p.id === poolId.value);

    if (pool) {
      // Get the product name
      const productResponse = await productApi.getById(pool.product);
      selectedPoolName.value = `Pool #${pool.id} (${productResponse.data.name})`;
    } else {
      selectedPoolName.value = `Pool #${poolId.value}`;
    }
  } catch (error) {
    console.error("Error loading pool name:", error);
    selectedPoolName.value = `Pool #${poolId.value}`;
  }
}

function openCreateDialog() {
  isEditing.value = false;
  editingRequestId.value = null;
  formEmail.value = "";
  formQuantity.value = 1;
  valid.value = false;
  dialog.value = true;
}

async function openEditDialog(request: Request) {
  isEditing.value = true;
  editingRequestId.value = request.id;
  formEmail.value = request.email;
  formQuantity.value = request.quantity;
  // Reset form validation state
  valid.value = false;
  // Wait for DOM to update before opening dialog
  await nextTick();
  dialog.value = true;
}

function closeDialog() {
  dialog.value = false;
  isEditing.value = false;
  editingRequestId.value = null;
  formEmail.value = "";
  formQuantity.value = 1;
}

async function saveRequest() {
  if (!valid.value) {
    console.log("Form validation failed, not submitting");
    return;
  }

  saving.value = true;
  try {
    await (isEditing.value && editingRequestId.value
      ? requestApi.update(poolId.value, editingRequestId.value, {
          email: formEmail.value,
          quantity: Number.parseInt(formQuantity.value.toString()),
        })
      : requestApi.create(poolId.value, {
          email: formEmail.value,
          quantity: Number.parseInt(formQuantity.value.toString()),
        }));
    closeDialog();
    await loadRequests();
  } catch (error: any) {
    console.error("Error saving request:", error);
    console.error("Error details:", error.response?.data);

    // Handle specific error cases
    if (error.response?.status === 400 && error.response?.data?.email) {
      alert(`Error: ${error.response.data.email}`);
    } else {
      alert("Error saving request. Please try again.");
    }
  } finally {
    saving.value = false;
  }
}

function deleteRequest(id: number) {
  requestToDelete.value = id;
  deleteDialog.value = true;
}

async function confirmDelete() {
  if (!requestToDelete.value) return;

  try {
    await requestApi.delete(poolId.value, requestToDelete.value);
    deleteDialog.value = false;
    requestToDelete.value = null;
    await loadRequests();
  } catch (error) {
    console.error("Error deleting request:", error);
    alert("Error deleting request. Please try again.");
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString();
}

function goBack() {
  router.push("/pools");
}

// Lifecycle
onMounted(async () => {
  if (poolId.value === 0) {
    console.error("Invalid pool ID, redirecting to pools page");
    router.push("/pools");
    return;
  }

  try {
    await loadPoolName();
    await loadRequests();
  } catch (error) {
    console.error("Error loading requests page:", error);
    alert("Error loading requests page. Please try again.");
  }
});
</script>
