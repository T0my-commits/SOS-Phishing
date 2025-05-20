<template>
    <div class="p-4 grid">
        <h1 class="text-center col-12">Designer le corps de l'email</h1>
        <div class="col-6">
            <div class="card">
                <div class="flex flex-column">
                    <label for="subject">Sujet</label>
                    <InputText id="subject" v-model="subject" />
                </div>
                <div class="flex flex-column">
                    <label for="userCode">Corps de l'email</label>
                    <Textarea id="userCode" v-model="userCode" rows="5" cols="30" />
                </div>
                <Button label="refresh" @click="actualizeCode()"></Button>
            </div>
        </div>
        <div class="col-6">
            <div class="card">
                <iframe :srcdoc="htmlContent" sandbox :key="iframe_key" class="w-full h-full"></iframe>
                <!-- <div v-html="htmlContent" :key="iframe_key"></div> -->
            </div>
        </div>
    </div>
  </template>
  
  <script>
  const blackListRegex = "/(<[^>]+>|<[^>]>|<\/[^>]+>)/ig";

  export default {
    data() {
        return {
            htmlContent: '',
            userCode: '',
            previewVisible: false,
            iframe_key: 0,
        }
    },
    methods: {
        showPreview() {
            this.previewVisible = true;
        },
        refreshIframe() {
            this.iframe_key += 1;
        },
        actualizeCode() {
            this.htmlContent = this.userCode.replace(blackListRegex, '');
        },
    }
  }
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  </style>
  