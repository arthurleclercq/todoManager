<template>
    <b-modal ref="loginModal" id="modal-login" title="Please log in to access your todo lists" hide-footer no-close-on-esc no-close-on-backdrop hide-header-close>
      <alert :message=message variant="danger" v-if="showMessage"></alert>
      <b-form @submit="onSubmit" class="w-100">
        <b-form-group id="form-login-group" label="Login:" label-for="form-login-input">
            <b-form-input id="form-login-input" type="text" v-model="login" required placeholder="Enter login">
            </b-form-input>
        </b-form-group>
        <b-form-group label="Password:" label-for="form-pwd-input">
            <b-form-input id="form-pwd-input" type="password" v-model="mdp" required placeholder="Enter password">
            </b-form-input>
        </b-form-group>
            <b-button-group>
                <b-button type="submit" variant="success">Log in</b-button>
                <b-button type="reset" @click="goAccount()" variant="info">I don't have an account yet</b-button>
            </b-button-group>
      </b-form>
    </b-modal>
</template>

<script>
import {AUTH_REQUEST} from '@/store/actions'
import Alert from '../components/Alert.vue'
export default {
    data() {
        return {
            login:'',
            mdp:'',
            message:'',
            showMessage:false
            
        }
    },
    methods: {
        goAccount(){
            this.$router.push(`/account`)
        },
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                user: this.login,
                password: this.mdp
            };
            this.tryLogin(payload);
        },
        tryLogin(payload){
            this.$store.dispatch(AUTH_REQUEST,payload)
                .then(() => {
                    this.$router.push("/")
                })
                .catch((error) => {
                    console.error(error);
                    this.message=error.message
                    this.showMessage=true
                });
        }

    },

    mounted(){
        this.$refs['loginModal'].show()
    },
    components: {
    alert: Alert
  },
}
</script>