<template>
    <div id="editor-mail-view">
        <div class="flex justify-content-center mb-3">
            <SelectButton v-model="editModeChoice" :options="options" aria-labelledby="basic" />
        </div>

        <section v-if="editModeChoice === 'Write text'">
            <InputText class="mb-3" v-model="sms_title" type="text" placeholder="Template title" />
            <Editor editorStyle="height: 300px" />
        </section>

        <section v-else-if="editModeChoice === 'Upload HTML'">
            <InputText class="mb-3" v-model="sms_title" type="text" placeholder="Template title" />
            <Toast />
            <FileUpload
                ref="fileUpload"
                name="demo[]"
                url="/api/upload"
                @upload="onUpload($event)"
                :multiple="false"
                fileLimit="1"
                invalidFileLimitMessage="One file max."
                :maxFileSize="1000000">
                <template #empty>
                    <span>Drag and drop files here to upload. (1 file max.)</span>
                </template>
            </FileUpload>
        </section>

        <section v-else class="flex justify-content-center">
            <p>Please select an option</p>
        </section>

    </div>
</template>

<script>
export default {
    data() {
        return {
            editModeChoice: 'Write text',
            options: ['Write text', 'Upload HTML']
        }
    },
    methods: {
        onUpload() {
            this.$toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
        }
    }
};
</script>
