import { defineStore } from 'pinia'
import { type GroupState , type Group , getGroupState } from './helper'
import { store } from '@/store'


export const useGroupStore = defineStore('group-store', {
  state: (): GroupState => getGroupState(),

  getters: {
    getListGRoup(state): Array<Group> {
      return state.list_group
    },
  },

  actions: {
    uploadData(list_group : Array<Group> ) {
      this.list_group = list_group
    },
    getNameGroup(group_id : string) : boolean | string {
      for( let group of this.list_group){
        if(group_id == group.group_id){
          console.log(group.group_name)
          return group.group_name
        }
      }
      return false
    }
    // addFriend(friend : string ){
        
    //     this.list_membership = [...this.list_membership,{ email : friend} ]
    // },
    // removeFriend(friend : string) {
    //     this.list_membership = this.list_membership.filter( (item : any) => {
    //        if (item.email != friend) {
    //         return item
    //        }
    //     } )


    // }

  },
})

