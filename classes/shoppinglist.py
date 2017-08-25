from flask import jsonify
from modals.modals import ShoppinlistModal, ItemModal


class Shoppinglist(object):
    """
    Handles all list operations
    """

    @staticmethod
    def create_list(name, desc, user_id):
        """
        Creates a new list
        :param name: 
        :param desc: 
        :param user_id: 
        :return: 
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 400
            return response

        mylist = ShoppinglistModal(name=name, desc=desc, user_id=user_id)
        if mylist.query.filter_by(name=name).first():
            response = jsonify({'Error': 'List name Already exists'})
            response.status_code = 400
            return response

        mylist.save()
        response = jsonify({
            'id': list.id,
            'name': list.name,
            'desc': list.desc,
            'user_id': list.user_id
        })
        response.status_code = 201
        return response

    @staticmethod
    def get_shoplists(user_id, search):
        """
        Gets all lists
        :param user_id: 
        :param search: 
        :return: 
        """
        response = ShoppinglistModal.query.all()
        if not response:
            response = jsonify({'error': 'No Lists has been created'})
            response.status_code = 200
            return response
        else:
            if search:
                res = [mylist for mylist in response if mylist.name
                       in search and mylist.user_id == user_id]
                if not res:
                    response = jsonify({
                        'error': 'The List you searched does not exist'
                    })
                    return response
                else:
                    shoppinglist_data = []
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                         
                            'user_id': data.user_id
                        }
                        shoppinglist_data.clear()
                        shoppinglist_data.append(final)
                    response = jsonify(shoppinglist_data)
                    response.status_code = 200
                    return response

            else:
                res = [mylist for mylist in
                       response if mylist.user_id == user_id]
                shoppinglist_data = []
                if not res:
                    response = jsonify({
                        'error': 'No lists have been created'
                    })
                    response.status_code = 200
                    return response
                else:
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                            'date_added': data.date_added,
                            'user_id': data.user_id
                        }
                        shoppinglist_data(final)
                    response = jsonify(shoppinglist_data)
                    response.status_code = 200
                    return response

    @staticmethod
    def get_single_list(user_id, list_id):
        """
        Gets single list
        :param user_id: 
        :param list_id: 
        """
        mylist = shoppinglist_data.query.filter_by(id=list_id,
                                             user_id=user_id).first()
        if not mylis:
            response = jsonify({
                'error': 'shoppinglist with id ' +
                         str(list_id) + ' not found'
            })
            response.status_code = 400
            return response

        list_data = {
            'id': list1.id,
            'name': mylist.name,
            'desc': mylist.desc,
            'user_id': mylist.user_id
        }
        response = jsonify(shoppinglist_data)
        response.status_code = 200
        return response

    @staticmethod
    def update_list(user_id, list_id, list_name, desc):
        """
        Updates ashoppinglist
                
        :param user_id: 
        :param list_id: 
        :param list_name: 
        :param desc:  
        """
        if not list_name:
            response = jsonify({'Error': 'Missing list name'})
            response.status_code = 400
            return response

        mylist = shoppinglist_data.query.filter_by(id=list_id,
                                             user_id=user_id).first()
        if not mylist:
            mylist = jsonify({'error': 'the list does not exist'})
            mylist.status_code = 400
            return mylist

        list1.name = list_name
        list1.desc = desc
        list1.update()

        mylist = ShoppinglistModal.query.filter_by(id=list_id,
                                             user_id=user_id).first()
        response = jsonify({
            'success': 'list updated',
            'mylist': list1.name
        })
        response.status_code = 200
        return response

    @staticmethod
    def delete_lists(user_id, list_id):
        """
        Deletes a list        
        :param user_id: 
        :param list_id: 
        """
        mylist = ShoppinglistModal.query.filter_by(id=list_id,
                                             user_id=user_id).first()
        if not mylists:
            response = jsonify({'error': 'list  not found'})
            response.status_code = 400
            return response

        items = ItemModal.query.filter_by(list_id=list_id)
        if items:
            for item in items:
                item.delete()

        mylist.delete()
        response = jsonify({
            'success': 'list deleted'
        })
        response.status_code = 200
        return response
