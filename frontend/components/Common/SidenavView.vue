<script setup>
import { getUserProfile, isAuthenticated, logoutUser } from '@/composables/useAuth';

const { data: user, error } = await useAsyncData('user', getUserProfile);

</script>

<template>
  <div id="mySidenav" class="sidenav">

    <!-- Logo -->
    <img src="/img/sos_logo_transparent_bgwhite.png" alt="Application Logo" width="240" class="h-0 m-auto mt-3 app-logo" />

    <!-- Menu (zone scrollable) -->
    <div class="flex-1 overflow-y-auto">
      <Menu :model="items" class="w-full">
        <template #submenuheader="{ item }">
          <span class="text-primary font-bold">{{ item.label }}</span>
        </template>
        <template #item="{ item, props }">
          <NuxtLink 
            :to="item.to" 
            v-ripple 
            v-bind="props.action"
            class="flex align-items-center cursor-pointer" 
            :class="{ 'menu-label': !('to' in item) }">
            <span v-if="item.icon" :class="item.icon" />
            <span class="ml-2">{{ item.label }}</span>
            <Badge v-if="item.badge" class="ml-auto" :value="item.badge" />
            <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
            <span v-if="item.items" class="pi pi-angle-down text-primary ml-auto" />
          </NuxtLink>
        </template>
      </Menu>
    </div>

    <!-- Zone utilisateur toujours visible en bas -->
    <div class="user-zone px-0 py-1 border-top-1 border-200 bg-white">
      <div v-if="user">
        <NuxtLink to="/user-profile" class="flex align-items-center cursor-pointer hover:surface-100 mt-2 mb-1">
          <span class="pi pi-user" />
          <span class="inline-flex flex-column">
            <span class="font-italic ml-2">{{ user.first_name + ' ' + user.last_name || user.username }}</span>
            <span class="text-sm">{{ user.role }}</span>
          </span>
        </NuxtLink>
        <NuxtLink @click="logoutUser(isToast=true); user=null" class="flex align-items-center cursor-pointer hover:surface-100 mt-1 mb-1">
          <span class="pi pi-chevron-circle-left" />
          <span class="ml-2">Sign Out</span>
        </NuxtLink>
      </div>
      <div v-else>
        <NuxtLink to="/login" class="flex align-items-center cursor-pointer hover:surface-100 mt-2 mb-1">
          <span class="pi pi-chevron-circle-right" />
          <span class="ml-2">Sign In</span>
        </NuxtLink>
      </div>
    </div>

  </div>
</template>


<script>
import Image from 'primevue/image';

export default {
  props: ['isSidenavVisibleBis'],
  watch: {
    isSidenavVisibleBis: function(newVal, oldVal) {
      this.toggleNav();
    },
  },
  data() {
    return {
      items: [
        {
          label: 'Test campaigns',
          items: [
            { label: 'New', icon: 'pi pi-plus ', to: '/new-test-campaign'},
            { label: 'Dashboards', icon: 'pi pi-folder-open', to: '/projects-dashboard' }
          ]
        },
        {
          label: 'Control campaigns',
          items: [
            { label: 'New', icon: 'pi pi-plus ', to: '/new-control-campaign'},
            { label: 'History', icon: 'pi pi-history', to: '' }
          ]
        },
        {
          label: 'Configuration',
          items: [
            { label: 'Employees samples', icon: 'pi pi-users', to: '' },
            { label: 'E-Mail templates', icon: 'pi pi-file-plus', to: '/email-templates' },
            { label: 'SMS templates', icon: 'pi pi-mobile', to: '/sms-templates' },
            { label: 'Fake websites', icon: 'pi pi-desktop', to: '' }
          ]
        },
        {
          label: 'Request tracking',
          items: [
            { label: 'New request', icon: 'pi pi-plus', to: '' },
            { label: 'History', icon: 'pi pi-history', to: '' }
          ]
        },
        {
          label: 'Newsletter',
          items: [
            { label: 'What\'s new?', icon: 'pi pi-star', to: '' },
            { label: 'How-To', icon: 'pi pi-question-circle', to: '' },
            { label: 'Awareness tickets', icon: 'pi pi-ticket', to: '' },
          ]
        },
        {
          label: 'Archived',
          items: [
            { label: 'My old campaign', icon: 'pi pi-folder', to: '/test' },
          ]
        },
      ],
      isSidenavVisible: true,
      isLargeScreen: true,
      widthSidenav: "290px",
    };
  },
  methods: {
    toggleNav() {
      this.isSidenavVisible = !this.isSidenavVisible;
      if (this.isSidenavVisible) {
        this.openNav();
      } else {
        this.closeNav();
      }
    },
    openNav() {
      document.getElementById("mySidenav").style.width = this.widthSidenav;
      //document.getElementById("myHeader").style.paddingLeft = "20px";
      document.getElementById("main-content").style.marginLeft = this.widthSidenav;
    },
    closeNav() {
      document.getElementById("mySidenav").style.width = "0";
      document.getElementById("myHeader").style.paddingLeft = "0";
      document.getElementById("main-content").style.marginLeft= "0";
    },
    checkScreenSize() {
      this.isLargeScreen = window.innerWidth >= 992;
      if (this.isSidenavVisible && this.isSidenavVisible !== this.isLargeScreen) {
        this.toggleNav();
      }
      this.isSidenavVisible = this.isLargeScreen;
    },
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkScreenSize);
  },
};
</script>

