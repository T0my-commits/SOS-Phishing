<script setup>
definePageMeta({
  middleware: 'auth'
})
</script>

<template>
    <div>
        <h2>E-Mail templates</h2>

        <!-- Tab bar -->
        <div class="grid">
            <div class="col-12">
                <div class="tabview-custom card flex flex-row flew-wrap justify-content-center p-3">
                    <Button @click="activeTab = 0" label="Default templates" class="w-full m-2" :outlined="activeTab !== 0" />
                    <Button @click="activeTab = 1" label="Custom templates" class="w-full m-2" :outlined="activeTab !== 1" />
                    <Button @click="activeTab = 2" label="Create new one" class="w-full m-2" :outlined="activeTab !== 2" />
                </div>
            </div>
            
            <div class="col-12">
                <div class="card">
                    <!-- Default templates -->
                    <ComponentItemGridView v-if="activeTab === 0" :apiUrl="templatesDefaultApiUrl" configMode=true />

                    <!-- Custom templates -->
                    <ComponentItemGridView v-if="activeTab === 1" :apiUrl="templatesDefaultApiUrl" configMode=true />

                    <!-- Create new one -->
                    <div v-if="activeTab === 2" class="flex flex-column justify-content-center mt-3 mb-3">
                        <form>
                            <EditorSmsView />
                            <div class="flex justify-content-end mt-3">
                                <Button label="Save" icon="pi pi-save" iconPos="right" />
                            </div>
                        </form>
                    </div>

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
            // API URLs
            templatesDefaultApiUrl: 'foo/',
            templatesCustomApiUrl: 'foo/',
            // var to delete
            toDeleteNbTemplate: 12,
        }
    }
}
</script>
