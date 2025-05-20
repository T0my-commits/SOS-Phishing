<script setup>
definePageMeta({
  middleware: 'auth'
})
</script>

<template>
    <div>
        <h2>Start new campaign</h2>

        <!-- Tab bar -->
        <div class="grid">
            <div class="col-12">
                <div class="tabview-custom card flex flex-row flew-wrap justify-content-center p-3">
                    <Button @click="activeTab = 0" label="E-Mail" class="w-full m-2" :outlined="activeTab !== 0" />
                    <Button @click="activeTab = 1" label="SMS" class="w-full m-2" :outlined="activeTab !== 1" />
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            // tabview custom
            activeTab: 0,
        }
    }
}
</script>
