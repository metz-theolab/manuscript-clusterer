<template>
  <v-app>
    <v-toolbar app>
      <span class="hidden-sm-and-up">
        <v-toolbar-side-icon @click="sidebar = !sidebar">
        </v-toolbar-side-icon>
      </span>
      <v-toolbar-title>
        <router-link to="/" tag="span" style="cursor: pointer">
          {{ appTitle }}
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-main>
      
      <v-content>
        <router-view />
      </v-content>
    </v-main>
  </v-app>
</template>

<script>
  export default {
    name: "App",
    data(){
      return {
        appTitle: 'Projector',
        menuItems: [
            { title: 'Home', path: '/', icon: 'home'},
            { title: 'Standard projection', path: '/project', icon: 'face' },
            { title: 'Experimental projection', path: '/experimental', icon: 'lock_open' },
            { title: 'Comparator', path: '/comparator', icon: 'compare' },
      ]
      }
    },
  };
</script>
