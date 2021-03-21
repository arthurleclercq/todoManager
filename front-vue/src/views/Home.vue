<template>
  <div >
    <div class="row">
      <div class="col-sm-12">
        <h1>Todo Lists</h1>
        <hr>
        <alert :message=message :variant=variant v-if="showMessage"></alert>
        <button id="bouton-add" type="button" class="btn btn-success btn-sm" v-b-modal.addList-modal>Add List</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" class="text-center">Name</th>
              <th scope="col" class="text-center">Todo number</th>
              <th scope="col" class="text-center">Last modification</th>
              <th scope="col" class="text-center">Actions</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(liste, index) in lists" :key="index">
              <td class="text-center">{{ liste.name }}</td>
              <td class="text-center">{{liste.todos.length}}</td>
              <td class="text-center">{{getLastModif(liste.todos)}}
              <td class="text-center">
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-success btn-sm" @click="go(liste.name)">See</button>
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.list-update-modal @click="editList(liste.name)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteList(liste.name)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addListModal"
            id="addList-modal"
            title="Add a new list"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Name:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addListName"
                        required
                        placeholder="Enter name">
          </b-form-input>
        </b-form-group>
       
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>


    <b-modal ref="editListModal"
         id="list-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="New name:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editListNewName"
                    required
                    placeholder="Enter name">
      </b-form-input>
    </b-form-group>
    
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-form>
</b-modal>
  </div>
</template>
<style scoped>
h1{
  padding-left:10px;
  padding-top:20px;
}

#bouton-add {
  margin-left: 5%;
}
</style>
<script>
import Alert from '../components/Alert.vue';
import axios from 'axios';

export default {
  data() {
    return {
      lists: [],
      addListName:'',
      editListNewName:'',
      editListOldName:'',
      deleteListName:'',
      message:'',
      variant:'',
      showMessage:false
    };
  },
  methods: {
    go(listename){
      this.$router.push(`/list/${listename}`)
    },
    getLastModif(todos){
      if (!todos.length){
        return "N/A"
      }
      return todos.reduce((acc,todo)=>Date.parse(acc.lastModif)>(Date.parse(todo.lastModif))?acc:todo).lastModif
    },
    getLists() {
      const path = 'http://localhost:5001/api/lists';
      axios.get(path)
        .then((res) => {
          this.lists = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  
    addList(payload) {
      const path = 'http://localhost:5001/api/lists';
      axios.put(path, payload)
        .then((res) => {
          this.getLists();
          this.message=res.data.message
          this.showMessage=true
          this.variant="success"
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.message=error.response.data.message
          this.showMessage=true
          this.variant="danger"
          this.getLists();
        });
    },
    initForm() {
      this.addListName=""
      this.editListNewName=""
      this.editListOldName=""
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addListModal.hide();
      const payload = {
        nom: this.addListName
      };
      this.addList(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addListModal.hide();
      this.initForm();
    },
    editList(list) {
      this.editListOldName = list;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editListModal.hide();
      const payload = {
        newName: this.editListNewName
      };
      this.updateList(payload, this.editListOldName);
    },
    updateList(payload, listOldName) {
      const path = `http://localhost:5001/api/list/${listOldName}`;
      axios.patch(path, payload)
        .then((res) => {
          this.getLists();
          this.message=res.data.message
          this.showMessage = true;
          this.variant="success"
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.message=error.response.data.message          
          this.showMessage = true;
          this.variant="danger"
          this.getLists();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editListModal.hide();
      this.initForm();
      this.getLists(); 
    },
    removeList(listName) {
      const path = `http://localhost:5001/api/list/${listName}`;
      axios.delete(path)
        .then((res) => {
          this.getLists();
          this.message=res.data.message
          this.showMessage = true;
          this.variant="success"
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.message=error.response.data.message          
          this.showMessage = true;
          this.variant="danger"
          this.getLists();
        });
    },
    onDeleteList(listName) {
      this.removeList(listName);
    },


  },
  
    created() {
      this.getLists();
    },
  components: {
    alert: Alert
  },
  
};
</script>