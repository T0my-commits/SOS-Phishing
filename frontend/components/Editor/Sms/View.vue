<template>
    <section id="editor-sms-view">

        <section>
            <InputText v-model="sms_title" type="text" size="large" placeholder="Large" />
            <Textarea v-model="sms_content" variant="filled" rows="5" cols="30" />
        </section>

    </section>
</template>

<script>
export default {
    data() {
        return {
            sms_title: '',
            sms_content: ''
        }
    }
};
</script>
