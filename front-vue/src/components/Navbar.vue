<template>
    
    <div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="/">Todo</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="/">Home</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        

        

        <b-nav-item-dropdown v-if="$store.getters.isAuthenticated" right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>{{$store.getters.username}}</em>
          </template>
          <b-dropdown-item href="#" @click="disconnect()">Log Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>

</template>
<script>
import {AUTH_LOGOUT} from '@/store/actions'
export default {
  name: 'Navbar',
  props: {},
  methods:{
      disconnect(){
          this.$store.dispatch(AUTH_LOGOUT)
          this.$router.push("/login")
      }
  }
}
</script>