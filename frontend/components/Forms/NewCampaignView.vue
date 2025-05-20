<template>
  <div class="grid">

    <!-- Stepper -->
    <div class="col-12 hidden md:block xl:block">
      <div class="card h-full">
        <Steps v-model:activeStep="activeStepId" :model="items" :readonly="false" />
      </div>
    </div>

    <div class="col-12">

      <!-- Step 1: General Information -->
      <!-- --------------------------- -->
      <div class="grid" v-if="activeStepId === 0">
        <!-- Fields -->
        <div class="col-12 md:col-12 xl:col-6">
          <div class="card flex flex-column h-full">
            <h3 class="md:hidden xl:hidden">Step 1: Global information</h3>

            <!-- Campaign name field -->
            <div class="flex flex-column gap-2">
              <label for="campaign-name">Campaign name</label>
              <InputText id="campaign-name" v-model="campaignName" aria-describedby="campaign-name-help" />
              <small id="campaign-name-help">Enter the name of the new campaign.</small>
            </div>

            <!-- Campaign type -->
            <p>Campaign type</p>
            <div class="flex justify-content-between">
              <SelectButton v-model="campaignTypeVal" :options="campaignTypeOpt" aria-labelledby="basic" />
            </div>

            <!-- Target specification -->
            <p>Targeted users</p>
              <MultiSelect v-model="selectedCities" :options="groupedCities" optionLabel="label" optionGroupLabel="label" optionGroupChildren="items" display="chip" filter
                placeholder="Select sample categories" class="w-full md:w-20rem">
                <template #optiongroup="slotProps">
                  <div class="flex align-items-center">
                    <img src="https://primefaces.org/cdn/primevue/images/flag/flag_placeholder.png"
                      :alt="slotProps.option.label" :class="`flag flag-${slotProps.option.code.toLowerCase()} mr-2`" style="width: 18px" />
                    <div>{{ slotProps.option.label }}</div>
                  </div>
                </template>
            </MultiSelect>

            <!-- Number of employees per sample -->
            <p>Percent of employees per sample</p>
            <div class="flex flex-wrap justify-content-start">
              <InputNumber v-model="percentOfEmployeesPerSample" 
                inputId="horizontal-buttons" showButtons buttonLayout="horizontal" :step="5" prefix="%" 
                :disabled="allEmployeesConcerned === 'true'" class="mb-3">
                <template #incrementbuttonicon>
                    <span class="pi pi-plus" />
                </template>
                <template #decrementbuttonicon>
                    <span class="pi pi-minus" />
                </template>
              </InputNumber>
              <!-- Button all employees concerned -->
              <div class="flex align-items-center gap-1 ml-3 mb-3">
                <Checkbox v-model="allEmployeesConcerned" inputId="allEmployeesConcerned" name="allEmployeesConcerned" value="true" />
                <label for="allEmployeesConcerned" class="ml-2"> All employees </label>
              </div>
            </div>

            <!-- Navigation buttons -->
            <FormsComponentsButtonStepper 
              prevBtn='false' nextBtn='true'
              v-on:stepForward="activeStepId += 1" v-on:stepBackward="activeStepId -= 1" />
          </div>
        </div>
        <!-- Decorator -->
        <div class="xl:col-6 hidden xl:block">
          <div class="card flex justify-content-center">
            <img src="@/public/img/signout/person-mozilla-1.jpg" class="w-full xl:w-8" />
          </div>
        </div>
      </div>

      <!-- Step 2: Templates -->
      <!-- ----------------- -->
      <div class="grid" v-if="activeStepId === 1">
        <!-- Fields -->
        <div class="col-12">
          <div class="card flex flex-column h-full">
            <h3 class="md:hidden xl:hidden">Step 2: Themes</h3>

            <!-- Select template type -->
            <div class="flex justify-content-center">
              <SelectButton v-model="templateTypeVal" :options="templateTypeOpt" aria-labelledby="basic" />
            </div>

            <!-- Choice 1: Default templates -->
            <ComponentItemGridView v-if="templateTypeVal === 'Default templates'" :apiUrl="templatesDefaultApiUrl" v-on:selectedId="FOO" />

            <!-- Choice 2: Custom templates -->
            <ComponentItemGridView v-else-if="templateTypeVal === 'Custom templates'" :apiUrl="templatesCustomApiUrl" v-on:selectedId="FOO" />

            <!-- Navigation buttons -->
            <FormsComponentsButtonStepper 
              prevBtn='true' nextBtn='true'
              v-on:stepForward="activeStepId += 1" v-on:stepBackward="activeStepId -= 1" />
          </div>
        </div>
      </div>

      <!-- Step 3: Redirect URL -->
      <!-- ----------------- -->
      <div class="grid" v-if="activeStepId === 2">
        <!-- Fields -->
        <div class="col-12">
          <div class="card flex flex-column h-full">
            <h3 class="md:hidden xl:hidden">Step 3: Redirect URl</h3>

            <!-- Select redirect URL template type -->
            <div class="flex justify-content-center">
              <SelectButton v-model="templateRedirectTypeVal" :options="templateRedirectTypeOpt" aria-labelledby="basic" />
            </div>

            <!-- Choice 1: None -->
            <div v-if="templateRedirectTypeVal === 'None'">
              <div class="flex flex-column m-auto justify-content-center align-items-center line-height-5 w-4 text-center">
                <p class="mt-5"><strong>No redirection</strong> is performed when the user is compromised. The victim will see an 'Error 404' page like.</p>
                <p>This option <strong>does not measure</strong> login information entered by an unwary user on malicious pages. To mesure this information, please select a <strong>template</strong> that supports this feature or <strong>manually create a fake malicious website</strong>.</p>
              </div>
            </div>


            <!-- Choice 2: Choose template -->
            <ComponentItemGridView v-else-if="templateRedirectTypeVal === 'Choose template'" :apiUrl="templatesDefaultApiUrl" />

            <!-- Choice 3: Edit manually -->
            <div v-else-if="templateRedirectTypeVal === 'Edit manually'" class="flex flex-column justify-content-center mt-3 mb-3">
              <div>
                <Editor v-model="value" editorStyle="height: 320px" class="w-full" />
              </div>
              <div class="mt-3">
                <Toast />
                <FileUpload name="demo[]" url="/api/upload" @upload="onAdvancedUpload($event)" :multiple="true" accept="image/*" :maxFileSize="1000000">
                  <template #empty>
                    <p>Drag and drop files to attach to e-mail.</p>
                  </template>
                </FileUpload>
              </div>
            </div>

            <!-- Choice 4: Enter URL -->
            <div v-else class="flex flex-column justify-content-center align-items-center">
              <div class="col-12 xl:col-6 align-items-center">
                <p>URL to redirect to user to: 
                  <i class="pi pi-info-circle"
                    v-tooltip="'Important: By choosing this option, you give up measuring login information entered by an unwary user on malicious website.'"></i>
                </p>
                <InputGroup>
                  <InputGroupAddon>www</InputGroupAddon>
                  <InputText placeholder="Website" />
                </InputGroup>
              </div>
            </div>

            <!-- Navigation buttons -->
            <FormsComponentsButtonStepper 
              prevBtn='true' nextBtn='true'
              v-on:stepForward="activeStepId += 1" v-on:stepBackward="activeStepId -= 1" />
          </div>
        </div>
      </div>

      <!-- Step 4: Configuration -->
      <!-- --------------------- -->
      <div class="grid" v-if="activeStepId === 3">
        <!-- Decorator -->
        <div class="xl:col-6 hidden xl:block">
          <div class="card flex justify-content-center">
            <img src="@/public/img/signout/person-mozilla-2.jpg" class="w-full xl:w-8" />
          </div>
        </div>
        <!-- Fields -->
        <div class="col-12 md:col-12 xl:col-6">
          <div class="card flex flex-column h-full">
            <h3 class="md:hidden xl:hidden">Step 3: Configuration</h3>
            
            <!-- Compromission proof -->
            <p>User is compromised when:</p>
            <div class="flex flex-wrap justify-content-start w-full">
              <Dropdown v-model="compromissionVal" :options="compromissionOpt" optionLabel="name" 
                placeholder="Select a trigger" />
            </div>

            <!-- Delayed delivery -->
            <p>Delayed delivery between messages 
              <i class="pi pi-info-circle info-icon"
                v-tooltip="'The delayed message strategy can be used to make each user believe that the message they receive is personally intended for them.'"></i>
            </p>
            <div class="flex flex-wrap justify-content-start">
              <InputNumber v-model="delayedDelivery" inputId="minmax-buttons" mode="decimal" showButtons :min="0" 
                suffix=" minutes" v-tooltip="'0 minutes means all messages are sent at the same time'" placeholder="Right" />
            </div>

            <!-- Notification when user is compromised -->
            <p>Send a notification to the following persons when compromission occurs (via SMS)</p>
            <div class="flex flex-wrap justify-content-start w-full">
              <MultiSelect v-model="personsToNotifyVal" display="chip" :options="personsToNotifyOpt" optionLabel="name"
                placeholder="Select a person to notify" :maxSelectedLabels="3" class="w-full md:w-20rem" />
            </div>

            <!-- Navigation buttons -->
            <FormsComponentsButtonStepper 
              prevBtn='true' nextBtn='submit'
              v-on:stepForward="" v-on:stepBackward="activeStepId -= 1" />
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
export default {
  name: 'FormsNewCampaignView',
  data() {
    return {
      // stepper var
      activeStepId: 0,
      items: [
        { label: 'Global information' },
        { label: 'E-Mail Template' },
        { label: 'Redirect to malicious website' },
        { label: 'Configuration' },
      ],
      // Campaign name
      campaignName: null,
      // Campaign type
      campaignTypeOpt: ['E-Mail', 'SMS'],
      campaignTypeVal: 'E-Mail',
      // Choose samples
      selectedCities: null,
      groupedCities: [
        {
          label: 'France',
          code: 'FR',
          items: [
            { label: 'Information Technologie dept.', value: 'IT_FR' },
            { label: 'Humain Resources dept.', value: 'RH_FR' },
            { label: 'Mechanics', value: 'Mechanics_FR' },
            { label: 'Dealers', value: 'Dealers_FR' },
            { label: 'Hotliners', value: 'Hotliners_FR' },
          ]
        },
        {
          label: 'Germany',
          code: 'DE',
          items: [
            { label: 'Humain Resources dept.', value: 'RH_DE' },
            { label: 'Mechanics', value: 'Mechanics_DE' },
          ]
        },
        {
          label: 'USA',
          code: 'US',
          items: [
            { label: 'Mechanics', value: 'Mechanics_US' },
            { label: 'Dealers', value: 'Dealers_US' },
            { label: 'Hotliners', value: 'Hotliners_US' },
          ]
        },
      ],
      // Percent of employees per samples
      percentOfEmployeesPerSample: 100,
      allEmployeesConcerned: false,
      // Choose template
      templateTypeOpt: ['Default templates', 'Custom templates'],
      templateTypeVal: 'Default templates',
      // Choose redirect URL type
      templateRedirectTypeOpt: ['None', 'Choose template', 'Edit manually', 'Enter URL'],
      templateRedirectTypeVal: 'None',
      // Delayed Delivery
      delayedDelivery: 0,
      // Compromission proof
      compromissionVal: null,
      compromissionOpt: [
        { name: 'User has opened the e-mail', code: 'NY' },
        { name: 'User has seen the image in the e-mail body', code: 'RM' },
        { name: 'User has downloaded the attachements', code: 'LDN' },
        { name: 'User has opened the attachements', code: 'IST' },
        { name: 'User has clicked on the link', code: 'PRS' },
        { name: 'User has fill some credentials', code: 'IST' },
      ],
      // Person to notify of each compromission
      personsToNotifyVal: null,
      personsToNotifyOpt: [
        { name: 'Valérie Dupieux', code: 'NY' },
        { name: 'Quentin Jérôme', code: 'RM' },
        { name: 'Marvin Malvob', code: 'LDN' },
        { name: 'Israël Sandoux', code: 'IST' },
      ],
      templatesDefaultApiUrl: '/api/default/templates',
      templatesCustomApiUrl: '/api/custom/templates',
    }
  },
  methods: {
    onAdvancedUpload() {
      this.$toast.add({ severity: 'info', summary: 'Success', detail: 'File Uploaded', life: 3000 });
    }
  }
};
</script>
