<script setup>
import { ref, onMounted } from 'vue'
import { useFetch, useCookie, useRuntimeConfig, useNuxtApp } from '#app'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { FilterMatchMode } from 'primevue/api'
import Skeleton from 'primevue/skeleton'
import { debugPrint } from '@/assets/js/debug';
import { getProjectsDashboard } from '@/composables/campaigns';

definePageMeta({
  middleware: 'auth'
})

const { $toast } = useNuxtApp()
const loadingCampaignsList = ref(true)
const campaignsList = ref(null)
const filters = ref({
  global: { 
    value: null, 
    matchMode: FilterMatchMode.CONTAINS 
  }
})

onMounted(async () => {
  loadingCampaignsList.value = true;
  campaignsList.value = await getProjectsDashboard();
  loadingCampaignsList.value = false;
});
</script>

<template>
  <div>
    <h2>Projects dashboard</h2>

    <div class="layout-content">
      <div class="grid">

        <!-- Current projects -->
        <div class="col-12">
          <div class="card flex flex-column gap-3">
            <span class="text-900 text-xl font-semibold">Current projects</span>

            <!-- Data table -->
            <transition name="fade">
              <DataTable v-if="!loadingCampaignsList && campaignsList && campaignsList.client_campaigns && campaignsList.client_campaigns.length > 0"
                :value="campaignsList.client_campaigns"
                :filters="filters"
                :globalFilterFields="['name', 'start_date', 'end_date', 'mode', 'type']"
                paginator
                :rows="5"
                :rowsPerPageOptions="[5, 10, 20, 50]"
                tableStyle="min-width: 50rem"
                paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
                currentPageReportTemplate="{first} to {last} of {totalRecords}"
              >
                <!-- Global search bar -->
                <template #header>
                  <div class="flex justify-content-end align-items-end">
                    <IconField iconPosition="left">
                      <InputIcon>
                        <i class="pi pi-search" />
                      </InputIcon>
                      <InputText v-model="filters['global'].value" placeholder="Search..." />
                    </IconField>
                  </div>
                </template>

                <template #paginatorstart>
                  <Button type="button" icon="pi pi-refresh" text @click="getProjectsDashboard()" />
                </template>

                <!-- Columns -->
                <Column field="name" header="Name" style="width: 14%">
                  <template #body="{ data }">
                    <NuxtLink :to="`/dashboard/${data.url_id}/`" class="no-underline font-bold text-600 hover:underline">
                      {{ data.name }}
                    </NuxtLink>
                  </template>
                </Column>
                <Column field="start_date" header="Start date" style="width: 14%" />
                <Column field="end_date" header="End date" style="width: 14%" />
                <Column field="mode" header="Mode" style="width: 14%" />
                <Column field="type" header="Type" style="width: 14%" />
                <Column field="messages_sent" header="Messages sent" style="width: 14%" />
                <Column field="targets_compromises" header="Compromises" style="width: 14%" />
              </DataTable>
            </transition>

            <!-- Placeholders -->
            <transition name="fade">
              <template v-if="loadingCampaignsList">
                <div class="flex flex-column gap-3">
                  <Skeleton height="2rem" width="10rem" />
                  <Skeleton height="2rem" />
                  <Skeleton height="2rem" />
                  <Skeleton height="2rem" />
                </div>
              </template>
            </transition>

            <!-- Information text -->
            <transition name="fade">
              <span v-if="!loadingCampaignsList && campaignsList && !campaignsList.client_campaigns?.length" class="m-auto w-full text-center mb-5">No current campaigns.</span>
            </transition>
          </div>
        </div>

          <!-- Archived projects -->
        <div class="col-12">
          <div class="card flex flex-column gap-3">
            <span class="text-900 text-xl font-semibold">Archived projects</span>

            <!-- Data table -->
            <DataTable v-if="!loadingCampaignsList  && campaignsList && campaignsList.client_archives && campaignsList.client_archives.length > 0"
              :value="campaignsList.client_archives"
              :filters="filters"
              :globalFilterFields="['name', 'start_date', 'end_date', 'mode', 'type']"
              paginator
              :rows="5"
              :rowsPerPageOptions="[5, 10, 20, 50]"
              tableStyle="min-width: 50rem"
              paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
              currentPageReportTemplate="{first} to {last} of {totalRecords}"
            >
              <!-- Global search bar -->
              <template #header>
                <div class="flex justify-content-end align-items-end">
                  <IconField iconPosition="left">
                    <InputIcon>
                      <i class="pi pi-search" />
                    </InputIcon>
                    <InputText v-model="filters['global'].value" placeholder="Search..." />
                  </IconField>
                </div>
              </template>

              <template #paginatorstart>
                <Button type="button" icon="pi pi-refresh" text @click="getProjectsDashboard()" />
              </template>

              <!-- Columns -->
              <Column field="name" header="Name" style="width: 14%">
                <template #body="{ data }">
                  <NuxtLink :to="`/dashboard/${data.url_id}/`" class="no-underline font-bold text-600 hover:underline">
                    {{ data.name }}
                  </NuxtLink>
                </template>
              </Column>
              <Column field="start_date" header="Start date" style="width: 14%" />
              <Column field="end_date" header="End date" style="width: 14%" />
              <Column field="mode" header="Mode" style="width: 14%" />
              <Column field="type" header="Type" style="width: 14%" />
              <Column field="messages_sent" header="Messages sent" style="width: 14%" />
              <Column field="targets_compromises" header="Compromises" style="width: 14%" />
            </DataTable>

            <!-- Placeholders -->
            <template v-else-if="loadingCampaignsList">
              <div class="flex flex-column gap-3">
                <Skeleton height="2rem" width="10rem" />
                <Skeleton height="2rem" />
                <Skeleton height="2rem" />
                <Skeleton height="2rem" />
              </div>
            </template>

            <!-- Information text -->
            <span v-else class="m-auto w-full text-center mb-5">No archived campaigns.</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>
