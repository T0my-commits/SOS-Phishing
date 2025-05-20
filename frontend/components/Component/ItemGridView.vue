<template>
    <div>
        <div class="flex flex-row flex-wrap justify-content-center align-items-center grid mt-3 mb-3">

            <!-- For each items, display it on a card with a label -->
            <CardImageView v-for="item in itemsList" class="col-12 md:col-6 lg:col-3 xl:col-3"
                :itemId="item.id"
                :itemName="item.name"
                :itemPreviewPath="item.previewPath"
                :itemLogoPath="item.logoPath"
                :itemIsNew="item.isNew"
                :isFakeWebsiteBinded="item.isFakeWebsiteBinded"
                :choosenId="choosenId"
                :configMode="configMode"
                v-on:selectedId="fSelectId" />

        </div>

        <!-- Paginator -->
        <Paginator :rows="10" :totalRecords="itemsList.length"></Paginator>
    </div>
</template>

<script>
export default {
    name: 'ManagementItemGridView',
    props: [
        'apiUrl',
        'configMode'
    ],
    data() {
        return {
            // selection mode for items
            choosenId: null,
            // defaults templates
            itemsList: [
                {
                    id: 0,
                    name: "Ameli security code",
                    previewPath: "/stub/templates/emails/ameli_code_securite.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: true,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 1,
                    name: "Doctolib feedback",
                    previewPath: "/stub/templates/emails/doctolib_feedback.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: true,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 2,
                    name: "Franceconnect connexion impots",
                    previewPath: "/stub/templates/emails/franceconnect_connexion_impots.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: true,
                    isFakeWebsiteBinded: false,
                },
                {
                    id: 3,
                    name: "Google new sign in",
                    previewPath: "/stub/templates/emails/google_new_sign_in.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: false,
                },
                {
                    id: 4,
                    name: "Instagram probleme connexion",
                    previewPath: "/stub/templates/emails/instagram_probleme_connexion.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 5,
                    name: "Leboncoin repondre message",
                    previewPath: "/stub/templates/emails/leboncoin_repondre_message.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 6,
                    name: "Linkedin invitations",
                    previewPath: "/stub/templates/emails/linkedin_invitations.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: false,
                },
                {
                    id: 7,
                    name: "Linkedin recommandation",
                    previewPath: "/stub/templates/emails/linkedin_recommandation.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 8,
                    name: "Paypal pub",
                    previewPath: "/stub/templates/emails/paypal_pub.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: true,
                },
                {
                    id: 9,
                    name: "Paypal pub",
                    previewPath: "/stub/templates/emails/paypal_pub.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: false,
                },
                {
                    id: 10,
                    name: "Paypal pub",
                    previewPath: "/stub/templates/emails/paypal_pub.png",
                    logoPath: "/stub/templates/emails/logo/logo_company.png",
                    isNew: false,
                    isFakeWebsiteBinded: true,
                },
            ],
        }
    },
    methods: {
        fSelectId(itemId) {
            if (this.choosenId === itemId) {
                this.choosenId = null;
            } else {
                this.choosenId = itemId;
            }
            this.$emit('selectedId', this.choosenId);
        }
    }
};
</script>
