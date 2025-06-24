<template>
    <div id="myHeader">
        <Menubar class="flex align-items-center justify-content-between">
            <template #start>
              <i class="pi pi-bars p-2 ml-2 mr-2 custom-sidenav-button" @click="$emit('toggle-sidenav', 'toggleNav')"></i>
            </template>
            <template #item="{ item, props, hasSubmenu, root }">
                <a v-ripple class="flex align-items-center" v-bind="props.action" :style="item.style">
                    <span :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                    <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                    <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{ item.shortcut }}</span>
                    <i v-if="hasSubmenu" :class="['pi pi-angle-down', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
                </a>
            </template>
            <template #end>
                <div class="flex align-items-center gap-2">
                    <Avatar icon="pi pi-user" class="mr-2" style="background-color: #dee9fc; color: #1a2551" shape="circle" />
                </div>
            </template>
        </Menubar>
    </div>
</template>

<script>
export default {
  name: 'HeaderView'
}
</script>
