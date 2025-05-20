<template>
    <div class="font-medium relative border-round-xl border-3 border-transparent" :key="itemId" :class="{'surface-100 border-primary-300': choosenId === itemId}">

        <!-- The card -->
        <div class="
            image-container
            border-2 surface-border border-round surface-ground 
            flex justify-content-center align-items-center
            m-1" style="height: 200px">
            <NuxtImg :src="itemPreviewPath" @click="itemClicked(itemId);" loading="lazy" class="preview-img"/>
        </div>

        <!-- Burger menu & buttons -->
        <div class="buttons-menu">
            <div v-if="configMode">
                <Button type="button" class="pi pi-bars" @click="showMenuItemPopup" aria-haspopup="true" aria-controls="overlay_tmenu"/>
                <TieredMenu ref="menuItem" id="overlay_tmenu" :model="itemsMenu" popup />
            </div>
            <span v-if="!(configMode)"
                v-tooltip.bottom="'Maximize'"
                class="pi pi-arrow-up-right-and-arrow-down-left-from-center border-round-xl"
                @click="this.isMaximizedImageVisible = true;">
            </span>
            <div v-if="isFakeWebsiteBinded">
                <span 
                    v-tooltip.bottom="'This template have a fake website associated to it that allows credentials stealing'" 
                    class="pi pi-desktop border-round-xl" style="color: darkturquoise;">
                </span>
            </div>
        </div>

        <!-- The label -->
        <div class="flex justify-content-center align-items-center pl-2 pr-2">
            <div class="flex justify-content-start align-items-center">
                <NuxtImg :src="itemLogoPath" width="30px" height="30px" loading="lazy" />
                <p class="ml-2 mr-1">{{ itemName }}</p>
                <Tag v-if="configMode && itemIsNew" class="ml-2" value="new"></Tag>
            </div>
        </div>

        <!-- Maximize image -->
        <Dialog v-model:visible="isMaximizedImageVisible" modal>
            <NuxtImg :src="itemPreviewPath" loading="lazy" class="preview-img"/>
        </Dialog>

        <!-- Metadata panel view -->
        <Sidebar v-model:visible="sidebarVisible" header="Details" position="right">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
        </Sidebar>

    </div>
</template>

<script>
export default {
    name: 'CardImageView',
    props: [
        'itemId',
        'itemName',
        'itemPreviewPath',
        'itemLogoPath',
        'itemIsNew',
        'isFakeWebsiteBinded',
        'choosenId',
        'configMode'
    ],
    data() {
        return {
            isMaximizedImageVisible: false,
            sidebarVisible: false,
            // menu items
            itemsMenu: [
                {
                    label: 'Maximize',
                    icon: 'pi pi-arrow-up-right-and-arrow-down-left-from-center',
                    command: () => { this.isMaximizedImageVisible = true; },
                },
                {
                    label: 'View details',
                    icon: 'pi pi-id-card',
                    command: () => { this.sidebarVisible = true; },
                },
                {
                    separator: true,
                },
                {
                    label: 'Download template',
                    icon: 'pi pi-download',
                },
            ],
        }
    },
    methods: {
        showMenuItemPopup(event) {
            this.$refs.menuItem.toggle(event);
        },
        itemClicked(itemId) {
            if (this.configMode) {
                this.isMaximizedImageVisible = true;
            } else {
                this.$emit('selectedId', this.itemId);
            }
        }
    }
}
</script>

<style scoped>
.buttons-menu {
    position: absolute;
    top: 17px;
    right: 17px;
    cursor: pointer;
}
.buttons-menu button, .buttons-menu span {
    width: 30px;
    height: 30px;
    padding: 7px 0px 7px 7px;
    margin: 3px;
    border: 2px;
    border-color: grey;
    color: black;
    background-color: var(--lightgrey-100);
}

.image-container {
    height: 100%;
    position: relative;
    overflow: hidden;
}
.image-container:hover {
    border: 2px solid red;
    cursor: pointer;
}
.image-container:hover .preview-img {
    height: 110%;
    transition: var(--transition-medium) all;
}

.image-container .preview-img {
    height: 100%;
    display: block;
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    transition: var(--transition-medium) all;
}
</style>
