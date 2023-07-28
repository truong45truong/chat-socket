import { defineStore } from 'pinia'
import { type MemberShipState , type MenberShip , getMemberShipState } from './helper'
import { store } from '@/store'


export const useMemberShipStore = defineStore('membership-store', {
  state: (): MemberShipState => getMemberShipState(),

  getters: {
    getListMemberShip(state): Array<MenberShip> {
      return state.list_membership
    },
  },

  actions: {
    uploadData(list_membership : Array<MenberShip> ) {
      this.list_membership = list_membership
    },
    checkMemberShip(user_to : MenberShip) : boolean{
        for( let item of this.list_membership){
            console.log("check friend" , item)
            if(item.email == user_to) return true
        }
        return false
    },
    addFriend(friend : string ){
        
        this.list_membership = [...this.list_membership,{ email : friend} ]
    },
    removeFriend(friend : string) {
        this.list_membership = this.list_membership.filter( (item : any) => {
           if (item.email != friend) {
            return item
           }
        } )


    }

  },
})

