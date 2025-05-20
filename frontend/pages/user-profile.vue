<script setup>
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import FileUpload from 'primevue/fileupload'
import Avatar from 'primevue/avatar'
import Chip from 'primevue/chip';

definePageMeta({
middleware: 'auth'
});

const user = ref({
firstName: '',
lastName: '',
phone: '',
mobile: '',
email: 'temp_account@test.com',
website: '',
about: '',
skype: '',
facebook: '',
twitter: '',
location: '',
})
</script>

<template>
  <div class="layout-content">
    <h2 class="text-2xl font-semibold">My Profile</h2>

    <div class="grid">
        <!-- Left: User Details -->
        <div class="col-12 md:col-4">
            <div class="card h-full">
                <Avatar icon="pi pi-user" class="mr-2 w-full h-full" style="background-color: #ece9fc; color: #2a1261" shape="circle" />
            </div>
        </div>

        <!-- Right: Image Uploads -->
        <div class="flex flex-column col-12 md:col-8 space-y-4 gap-3">
            <!-- General information -->
            <div class="card h-full">
                <h3 class="text-lg font-medium mb-4">General information</h3>
                <div class="flex flex-column gap-3">
                    <div class="flex flex-col gap-2">
                        <label for="username">First Name</label>
                        <InputText id="first_name" v-model="user.firstName" aria-describedby="username-help" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="username">Last Name</label>
                        <InputText id="last_name" v-model="user.lastName" aria-describedby="username-help" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="username">Last logged in</label>
                        <span>7 May 2025 11:06:12 am</span>
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="username">Role</label>
                        <Chip class="py-0 pl-0 pr-4">
                            <span class="ml-2 font-medium">Admin</span>
                        </Chip>
                    </div>
                </div>
            </div>

            <!-- Contact information -->
            <div class="card h-full">
                <h3 class="text-lg font-medium mb-4">Contact information</h3>
                <div class="flex flex-column gap-3">
                    <div class="flex flex-col gap-2">
                        <label for="username">E-mail</label>
                        <InputText id="first_name" v-model="user.firstName" aria-describedby="username-help" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="username">Phone</label>
                        <InputText id="last_name" v-model="user.lastName" aria-describedby="username-help" />
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>
</template>

<style scoped>
.card {
@apply bg-white p-5 rounded-lg shadow-md;
}
</style>
  