<script setup>
import { inject } from 'vue';
import { useFetch, showError,   useCookie, useRuntimeConfig, useNuxtApp } from '#app';
import { useRoute } from 'vue-router';
import { debugPrint } from '@/assets/js/debug';
import { getCampaignInfo, getRecentActivities } from '@/composables/campaigns';
import { FilterMatchMode } from 'primevue/api'

const route = useRoute();

const { $toast } = useNuxtApp()
const url_id = route.params.url_id;
const loadingCampainInfo = ref(true);
const campaignInfo = ref(null);
const loadingRecentActivities = ref(true)
const recentActivities = ref(null)
const filters = ref({
  global: { 
    value: null, 
    matchMode: FilterMatchMode.CONTAINS 
  }
})

// Check validity of url_id
const isValidId = /^[a-z0-9-]+$/.test(url_id);
if (!isValidId) {
  throw showError({
    statusCode: 404,
    statusMessage: 'Page not found'
  });
};

// Header configuration
// const setHeaderItems = inject('setHeaderItems');
// if (setHeaderItems) {
//   setHeaderItems([
//     { label: 'Dashboard', icon: 'pi pi-home' },
//     { label: 'Settings', icon: 'pi pi-cog' },
//     { label: 'Stop campaign', icon: 'pi pi-stop', style: 'color: var(--red-300);' }
//   ]);
// }

// Fetch informations
onMounted(async () => {
  // Information cards
  loadingCampainInfo.value = true;
  campaignInfo.value = await getCampaignInfo(url_id);
  loadingCampainInfo.value = false;

  // Recent activity
  loadingRecentActivities.value = true;
  recentActivities.value = await getRecentActivities(url_id);
  loadingRecentActivities.value = false;
});
</script>

<template>
  <div>
    <h2>Dashboard</h2>
    <div class="layout-content">
      <div class="grid">

        <!-- Information cards -->
        <div class="col-12 md:col-6 sm:col-6 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo"
            title="Payloads Sent" 
            :text_big="`${campaignInfo?.sent ?? '—'}`" 
            text_medium="" 
            text_small="" 
            :subtitle_nb="`${campaignInfo?.percentage_to_be_sent ?? '—'}% `" 
            subtitle_nb_color="text-green-500" 
            subtitle_text="must be sent" 
            icon="bi bi-send text-blue-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-6 sm:col-6 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Compromises" 
            :text_big="`${campaignInfo?.compromises ?? '—'}`"
            text_medium="" 
            text_small=" persons"
            subtitle_text="of compromises"
            :subtitle_nb="`${campaignInfo?.percentage_compromises ?? '—'}% `" 
            subtitle_nb_color="text-red-500"
            icon="bi bi-exclamation-triangle text-red-500"
            />
          </div>
        </div>
        <div class="col-12 md:col-3 sm:col-6 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Signaling" 
            :text_big="`${campaignInfo?.percentage_current_signaling ?? '—'}`" 
            text_medium="%" 
            text_small="" 
            :subtitle_nb="`${campaignInfo?.percentage_expected_signaling ?? '—'}% `" 
            subtitle_nb_color="text-yellow-500" 
            subtitle_text="expected as success" 
            icon="bi bi-person-bounding-box text-yellow-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-3 sm:col-6 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
              :isLoading="loadingCampainInfo" 
              title="Servers" 
              text_big="0" 
              text_medium="" 
              text_small=" in use" 
              subtitle_nb="" 
              subtitle_nb_color="text-green-500" 
              subtitle_text="since beginning" 
              icon="bi bi-server text-cyan-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-3 sm:col-6 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
              :isLoading="loadingCampainInfo" 
              title="Feedbacks" 
              :text_big="`${campaignInfo?.percentage_feedbacks ?? '—'}`" 
              text_medium="%" 
              text_small="" 
              :subtitle_nb="`${campaignInfo?.feedbacks ?? '—'} `" 
              subtitle_nb_color="text-green-500" 
              subtitle_text="feedbacks collected" 
              icon="bi bi-chat-square-dots text-green-400" 
            />
          </div>
        </div>
        <div class="col-12 md:col-3 sm:col-6 xl:col-2">
          <div class="card h-full">
              <CardInformationView 
                :isLoading="loadingCampainInfo" 
                title="Duration of test" 
                :text_big="`${campaignInfo?.hours_elapsed ?? '—'} `" 
                text_medium="" 
                text_small="hours" 
                :subtitle_nb="`${campaignInfo?.hours_remaining ?? '—'}h `" 
                subtitle_nb_color="text-yellow-600" 
                subtitle_text="remaining" 
                icon="bi bi-clock text-yellow-500" 
              />
          </div>
        </div>

        <!-- Bar chart -->
        <div class="col-12 xl:col-8">
          <div class="card h-full">
            <DashboardChartCompromisesByDateView />   
          </div>
        </div>

        <!-- Pie chart -->
        <div class="col-12 xl:col-4">
          <div class="card h-full">
            <DashboardChartCompromisesByCategoriesView />
          </div>
        </div>

        <!-- Campaign stats -->
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo"
            title="Clicks on link" 
            :text_big="`${campaignInfo?.clicks ?? '—'}`" 
            text_medium="" 
            text_small=" clicked" 
            subtitle_nb="" 
            subtitle_nb_color="text-green-500" 
            subtitle_text="" 
            icon="bi bi-mouse2 text-orange-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Download attachments" 
            :text_big="`${campaignInfo?.download_attachments ?? '—'}`"
            text_medium="" 
            text_small=" downloaded"
            subtitle_text=""
            subtitle_nb="" 
            subtitle_nb_color="text-red-500"
            icon="bi bi-envelope-paper text-purple-600"
            />
          </div>
        </div>
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Open attachments" 
            :text_big="`${campaignInfo?.open_attachments ?? '—'}`" 
            text_medium="" 
            text_small=" opened" 
            subtitle_nb="" 
            subtitle_nb_color="text-yellow-500" 
            subtitle_text="" 
            icon="bi bi-envelope-paper text-pink-600" 
            />
          </div>
        </div>
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Credentials" 
            :text_big="`${campaignInfo?.creds_leak ?? '—'}`" 
            text_medium="" 
            text_small=" leaked" 
            subtitle_nb="" 
            subtitle_nb_color="text-green-500" 
            subtitle_text="" 
            icon="bi bi-person-vcard text-green-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Signalisations" 
            :text_big="`${campaignInfo?.reports ?? '—'}`" 
            text_medium="" 
            text_small=" collected" 
            subtitle_nb="" 
            subtitle_nb_color="text-green-500" 
            subtitle_text="" 
            icon="bi bi-exclamation-circle text-yellow-500" 
            />
          </div>
        </div>
        <div class="col-12 md:col-4 sm:col-4 xl:col-2">
          <div class="card h-full">
            <CardInformationView 
            :isLoading="loadingCampainInfo" 
            title="Attack vector" 
            text_big="" 
            :text_medium="`${campaignInfo?.mode ?? '—'}`" 
            text_small="" 
            subtitle_nb="" 
            subtitle_nb_color="text-yellow-600" 
            subtitle_text="" 
            icon="bi bi-arrows-move text-cyan-500" 
            />
          </div>
        </div>

        <!-- List Activities -->
        <div class="col-12">
          <div class="card h-full flex flex-column gap-3">
            <span class="block text-800 font-medium text-left mb-3">Recent Activities</span>

            <!-- Data table -->
            <transition name="fade">
              <DataTable v-if="!loadingRecentActivities && recentActivities && recentActivities.length > 0"
                :value="recentActivities"
                :filters="filters"
                :globalFilterFields="['job_type', 'place_of_work', 'country', 'event_label', 'event_date', 'payload_sent_at', 'interests']"
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
                <Column field="country" header="Country" style="width: 14%" />
                <Column field="place_of_work" header="Place of work" style="width: 14%" />
                <Column field="job_type" header="Job type" style="width: 14%" />
                <Column field="interests" header="Interests" style="width: 14%">
                  <template #body="{ data }">
                    {{ data.interests?.join(', ') }}
                  </template>
                </Column>
                <Column field="payload_sent_at" header="Payload sent at" style="width: 14%" />
                <Column field="event_date" header="Event date" style="width: 14%" />
                <Column field="event_label" header="Activity" style="width: 14%" />
              </DataTable>
            </transition>

            <!-- Placeholders -->
            <transition name="fade">
              <template v-if="loadingRecentActivities">
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
              <span v-if="!loadingRecentActivities && recentActivities && !recentActivities?.length" class="m-auto w-full text-center mb-5">No current campaigns.</span>
            </transition>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'primevue/chart';
import { ref } from "vue";

const optionsMenuVisible = ref(false);
const sidebarVisible = ref(true);
</script>
