from graphene_django import DjangoObjectType
import graphene 
from apps.decks.models import Deck as DeckModel
from apps.cards.models import Card as CardModel


from apps.user.models import User as UserModel

class User(DjangoObjectType):
    class Meta:
        model = UserModel

class Deck(DjangoObjectType):
    class Meta:
        model = DeckModel

class Card(DjangoObjectType):
    class Meta:
        model = CardModel


class CreateCard(graphene.Mutation):
    card = graphene.Field(Card)
    
    class Arguments:
        question = graphene.String()
        answer = graphene.String()
        deck_id = graphene.Int()


    def mutate(self, info, question, answer, deck_id):
        card_mut = CardModel(question = question, answer = answer)
        deck_to_store = DeckModel.objects.get(id = deck_id)
        card_mut.deck = deck_to_store
        card_mut.save()
        return CreateCard(card = card_mut)

class CreateDeck(graphene.Mutation):
    deck = graphene.Field(Deck)    

    class Arguments:
        title = graphene.String()
        description = graphene.String()


    def mutate(self, info, title, description):
        deck_mut = DeckModel(title = title, description = description)
        deck_mut.save()
        return CreateDeck(deck = deck_mut)

class updateCard(graphene.Mutation):
    card = graphene.Field(Card)
    class Arguments:
        id = graphene.Int()
        question = graphene.String()
        answer = graphene.String()
        deck_id = graphene.Int()


    def mutate(self, info, id, question=None, answer=None, deck_id=None):
        card_update = CardModel.objects.get(id=id)
        card_update.question = question if question is not None else card_update.question
        card_update.answer = answer if answer is not None else card_update.answer       
        if deck_id is not None:
            deck_to_change = DeckModel.objects.get(id = deck_id)
            card_update.deck = deck_to_change
        card_update.save()
        return CreateCard(card = card_update)




class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    create_deck = CreateDeck.Field()
    update_card = updateCard.Field()
        
class Query(graphene.ObjectType):
    users = graphene.List(User)
    cards = graphene.List(Card)
    decks = graphene.List(Deck)
    deck_card = graphene.List(Card, deck = graphene.Int())  # passing deck id for card 

    def resolve_users(self, info):
        return UserModel.objects.all()

    def resolve_decks(self, info):
        return DeckModel.objects.all()
    
    def resolve_deck_card(self, info, deck):
        return CardModel.objects.filter(deck=deck)

    def resolve_cards(self, info):
        return CardModel.objects.all()
        
Schema = graphene.Schema(query=Query, mutation = Mutation)
