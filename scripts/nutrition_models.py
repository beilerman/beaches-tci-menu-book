"""Explicit models for the pinned menu inventory, authored 2026-10-26.

Numbers reference the immutable inventory snapshot, never fuzzy/keyword matches.
Weights are hypothetical edible grams, not observed resort portions. Prepared USDA
foods include their own fat/sauce; added components represent listed accompaniments.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / 'data/nutrition/menu-inventory.json'
ROWS = json.loads(INVENTORY.read_text())
INVENTORY_SHA256 = '4509017b890f5ce01670379a26534494e7468373f4df853a18ec7e85c94224e1'
if hashlib.sha256(INVENTORY.read_bytes()).hexdigest() != INVENTORY_SHA256:
    raise ValueError('Menu inventory changed: review all explicit row assignments before rebuilding')
MODELS = {}

# FoodData Central FNDDS 2021-2023 IDs. Aliases are explicit reviewed selections.
IDS = {
 'milk':2705385,'condensed':2705402,'yogurt':2705426,'greek':2705430,
 'cream':2705597,'whipped':2705598,'sourcream':2705614,'icecream':2705630,
 'custard':2705682,'flan':2705683,'brulee':2705684,'chocpudding':2705679,
 'bluecheese':2705705,'cheddar':2705709,'feta':2705714,'goatcheese':2705716,
 'gouda':2705717,'gruyere':2705718,'mozzarella':2705722,'parmesan':2705728,
 'provolone':2705733,'swiss':2705735,'paneer':2705740,'ricotta':2705750,
 'american':2705764,'alfredo':2705809,'steak':2705836,'flank':2705827,
 'ribeye':2705829,'tbone':2705839,'filet':2705841,'shortrib':2705845,
 'beef':2705854,'patty':2705855,'porkchop':2705867,'ham':2706206,
 'prosciutto':2705879,'pork':2705882,'canadian':2705884,'bacon':2705889,
 'ribs':2705894,'belly':2705901,'lamb':2705906,'veal':2705909,
 'chicken':2705956,'friedchicken':2705975,'chickenleg':2705984,
 'wings':2706068,'nuggets':2706094,'duck':2706139,'hen':2706145,
 'pate':2706155,'hotdog':2706167,'sausage':2706191,
 'whitefish':2706325,'friedfish':2706327,'snapper':2706283,
 'salmon':2706286,'rawsalmon':2706284,'smokedsalmon':2706292,
 'bass':2706295,'swordfish':2706301,'rawtuna':2706308,'tuna':2706310,
 'octopus':2706331,'clams':2706342,'crab':2706344,'lobster':2706349,
 'mussels':2706350,'scallops':2706356,'shrimp':2706363,'friedshrimp':2706364,
 'crabcake':2706549,'egg':2707154,'friedegg':2707159,'omelet':2707201,
 'beans':2707349,'bakedbeans':2707391,'hummus':2707402,'lentils':2707425,
 'tofu':2707435,'soy':2707442,'teriyaki':2707445,'misosoup':2707455,
 'lentilsoup':2707462,'veganlink':2707467,'veganchicken':2707468,
 'veggiepatty':2707473,'almonds':2707485,'cashews':2707493,'coconut':2707500,
 'peanuts':2707512,'pecans':2707521,'pistachio':2707527,'walnuts':2707531,
 'peanutbutter':2707537,'coconutmilk':2707568,'coconutcream':2707571,
 'coconutwater':2707572,'tahini':2707587,'bread':2707610,'focaccia':2707612,
 'naan':2707613,'pita':2707616,'bun':2707657,'dogbun':2707656,
 'cinnamonroll':2707668,'croissant':2707678,'bagel':2707684,'muffin':2707698,
 'wheatbread':2707709,'tortilla':2707824,'corntortilla':2707823,
 'cheesecake':2707861,'choccheesecake':2707863,'choccake':2707866,
 'shortcake':2707896,'brownie':2707904,'applepie':2707995,'cherrypie':2707999,
 'lemontart':2708000,'choctart':2708005,'nutpie':2708015,'fritter':2708024,
 'eclair':2708031,'puff':2708053,'danish':2708060,'churro':2708070,
 'chips':2708202,'pancake':2708294,'frenchtoast':2708333,'dumpling':2708344,
 'pasta':2708357,'grits':2708374,'oatmeal':2708381,'quinoa':2708400,
 'rice':2710788,'bulgur':2708438,'couscous':2708441,'granola':2708461,
 'pizza':2708615,'pepperonipizza':2708639,'meatpizza':2708650,
 'vegpizza':2708629,'eggroll':2708700,'potsticker':2708705,'shumai':2708708,
 'gnocchi':2708722,'bao':2708725,'lasagna':2708752,'mac':2708811,
 'friedrice':2708951,'ricebeans':2709033,'coconutrice':2709032,
 'banana':2709224,'mango':2709242,'pineapple':2709260,'watermelon':2709270,
 'fruit':2709288,'lime':2709184,'pineapplejuice':2709329,'cranberry':2710579,
 'fries':2709462,'hashbrown':2709480,'mashed':2709500,'bakedpotato':2709524,
 'plantain':2709559,'plantainchips':2709563,'spinach':2709615,
 'creamedspinach':2709628,'broccoli':2709645,'carrot':2709664,
 'pumpkin':2709692,'sweetpotato':2709699,'sweetmash':2709708,
 'sweetfries':2709713,'tomato':2709719,'bbq':2709750,'cucumber':2709784,
 'mushroom':2709937,'salad':2709822,'slaw':2709815,'cauliflower':2709897,
 'corn':2709910,'seaweed':2710100,'butter':2710155,'hollandaise':2710171,
 'pesto':2710175,'oil':2710186,'sesameoil':2710190,'bluecheesedressing':2710197,
 'caesardressing':2710199,'dressing':2710203,'mayo':2710204,
 'sugar':2710258,'syrup':2710273,'chocsyrup':2710276,'caramel':2710284,
 'sweetsour':2710296,'coffee':2710375,'espresso':2710378,'latte':2710386,
 'mocha':2710410,'icedlatte':2710431,'cappuccino':2710472,'tea':2710490,
 'tonic':2710538,'liqueur':2710623,'creamliqueur':2710624,
 'coffeeliqueur':2710625,'daiquiri':2710630,'sparkling':2710687,
 'wine':2710688,'sake':2710691,'meringue':2707297,'onionrings':2710055,
 'avocado':2709223,'beet':2709872,'broth':2707132,'cake':2707886,
 'celery':2709778,'chocolate':2710328,'cookie':2707964,'creamcheese':2705760,
 'dates':2709203,'edamame':2707436,'eel':2706247,'eggplant':2709929,
 'gravy':2707145,'marshmallow':2710353,'oats':2708489,'olives':2710088,
 'onion':2709950,'orangejuice':2709186,'peas':2709959,'potato':2709388,
 'raisins':2709212,'scalloped':2709449,'seafoodsoup':2707143,'soda':2710555,
 'spirit':2710703,'sweetmuffin':2707830,'waffle':2708320,
}

def put(indices, spec, serving='One assumed plated serving; listed accompaniments included', note=''):
    if isinstance(indices, int): indices = [indices]
    components = []
    for token in spec.split():
        alias, amount = token.split('=')
        vals = [float(x) for x in amount.split('/')]
        if len(vals) == 1:
            x = vals[0]
            # Deliberately broad scenario amounts; not a statistical confidence interval.
            vals = [round(x * .65, 2), x, round(x * 1.5, 2)]
        if len(vals) != 3 or not 0 <= vals[0] <= vals[1] <= vals[2]:
            raise ValueError(token)
        components.append({'profile':alias, 'grams':vals})
    for i in indices:
        if i in MODELS: raise ValueError(f'Duplicate assignment {i}')
        MODELS[i] = dict(components=copy.deepcopy(components), serving=serving, note=note)

def same(indices, original, note=None):
    if isinstance(indices,int): indices=[indices]
    for i in indices:
        if i in MODELS: raise ValueError(f'Duplicate assignment {i}')
        MODELS[i]=copy.deepcopy(MODELS[original])
        if note is not None: MODELS[i]['note']=note

def unavailable(indices, reason):
    if isinstance(indices,int): indices=[indices]
    for i in indices:
        if i in MODELS: raise ValueError(f'Duplicate assignment {i}')
        MODELS[i]={'withheld_reason':reason}

# Pinta: estimates refer to individual counter orders, not a whole buffet plate.
put([0,381,255], 'conch=90 salad=90 lime=20', 'One assumed small conch salad/ceviche, about 200 g', 'Cooked USDA conch is a proxy; the citrus-marinated preparation is not measured.')
put(1,'fritter=35 conch=10 mayo=10','One assumed fritter, with dipping sauce','Plain fritter plus conch proxy; size and oil uptake unknown.')
put([2,51],'conch=120 bread=30 oil=15 mayo=25','One assumed fried-conch order with sauce','Bread represents flour coating; oil is assumed retained frying oil, not cooking-pan oil.')
put(3,'sausage=75 pork=100 chickenleg=120 bbq=25','One assumed mixed-meat platter; no unlisted sides')
put([4,53],'pork=120 salad=160 avocado=50 bluecheese=25 corn=40 bluecheesedressing=30')
put(5,'chicken=100 salad=160 pineapple=60 dressing=30')
put(6,'patty=150 bun=75 american=25 pineapple=30 mayo=25 salad=25','One assumed burger; no unlisted fries')
put([7,54],'beans=100 tahini=20 tofu=30 oil=10 pita=70')
put([8,55],'rice=110 beans=45 coconutmilk=30','One assumed side, about 185 g','Rice, beans and coconut milk are ingredient proxies, not a measured recipe.')
put([9,56],'plantain=100','One assumed side of fried plantain, 65–150 g')
put([10,68,231,232,349,350],'pizza=350','One assumed whole individual pizza, 230–525 g; not per slice','Pizza diameter and dough weight are unknown. USDA thin-crust cheese pizza is a prepared-food proxy.')
put(11,'pepperonipizza=350 syrup=20','One assumed whole individual pizza; not per slice')
put([12,234,355],'meatpizza=380','One assumed whole individual pizza; not per slice')
put(13,'pizza=330 chicken=70 gouda=25 oil=10','One assumed whole individual pizza; not per slice','Cheese pizza proxy plus chicken, extra cheese and garlic oil.')
put(14,'pizza=330 bakedpotato=70 bacon=20 sourcream=30','One assumed whole individual pizza; not per slice')
put(15,'pizza=330 mushroom=60 ricotta=40 oil=8','One assumed whole individual pizza; not per slice')
put(16,'pasta=220 clams=80 oil=15','One assumed pasta entrée; no bread')
put([17,62],'pasta=220 tomato=80 cream=60 parmesan=15 butter=10 mushroom=40')
put([18,63],'pasta=220 beef=80 pork=40 tomato=100 oil=8')
put(19,'friedshrimp=70 friedfish=100 onionrings=40 mayo=25','One assumed fried-seafood starter','Fried fish substitutes for calamari; species, batter and oil vary.')
put(20,'bread=120 ham=40 sausage=50 provolone=30 salad=40','One assumed sandwich; no unlisted side','Sausage is a proxy for salami and pepperoni.')
put(21,'tomato=150 mozzarella=80 oil=12 syrup=10')
put([22,66],'pasta=200 butter=25','One assumed bowl; no unlisted sides')
put(23,'olives=50 ricotta=50 bread=60 oil=8')
put([24,67],'bread=70 butter=18','One assumed two-piece garlic bread order')
put(25,'shrimp=140 broccoli=80 peanuts=25 sweetsour=40 oil=10','One assumed entrée without added rice')
put([26,76],'pasta=220 egg=50 salad=70 peanuts=20 sweetsour=40 oil=15','One assumed base Pad Thai; optional meat/shrimp excluded','Cooked wheat pasta is an energy proxy for cooked rice noodles; noodle hydration and tamarind sauce vary.')
put(27,'friedchicken=160','One assumed karaage order; no unlisted rice')
put([28,75],'beef=140 broccoli=100 teriyaki=35 oil=10','One assumed entrée; no unlisted rice')
put([29,77],'friedrice=220','One assumed base fried-rice bowl; optional meat/shrimp excluded')
put(30,'potsticker=120','Assumed three potstickers with a combined edible weight of 80–180 g')
unavailable(31,'Pork and shrimp are alternatives, and the number/size of dumplings is unspecified. Choose a filling and piece count first.')
put(32,'bao=60 beef=55 american=15 mayo=12 salad=20','One assumed bao bun')
put([33,80],'eggroll=60','One assumed vegetable spring roll','USDA meatless egg roll is a prepared-food proxy.')
put(34,'cucumber=140 sesameoil=8 soy=10 sugar=5')
put(35,'pasta=180 salad=100 sesameoil=15 soy=15')
put([36,85],'tortilla=30 pork=50 avocado=20 sourcream=15 salad=15','One taco, as listed; assumed filling weights')
put([37,86],'tortilla=30 chicken=50 tomato=20 salad=20 oil=4','One taco, as listed; assumed filling weights')
put(38,'tortilla=30 flank=55 salad=30','One taco, as listed; assumed filling weights')
put([39,87],'tortilla=30 pumpkin=60 mushroom=30 oil=8 tomato=20','One taco, as listed; assumed filling weights')
unavailable(40,'This row groups cheese, chicken and beef quesadillas. Filling and piece size must be selected before assigning calories.')
put(41,'shrimp=90 avocado=40 tomato=70 chips=30')
put([42,88],'chips=65 cheddar=50 milk=30 beef=50 tomato=40')
put([43,89],'corn=120 sourcream=20 parmesan=10 mayo=15','One assumed ear of corn, edible kernels and toppings only')
put(44,'churro=65 chocsyrup=25 caramel=20','One assumed churro plus shared dipping sauces','Chocolate syrup represents the chocolate sauces; white chocolate can be richer.')
unavailable([45,46,47,91,92,93],'This is a list of different drinks or bottles, not one fixed serving. Recipe, selection and pour are required.')
put(48,'shrimp=140 grits=150 coconutmilk=45 salad=35 butter=10')
put(49,'chickenleg=170 carrot=80 coconutmilk=100 rice=130 beans=50 plantain=70 syrup=20')
put(50,'lamb=180 sweetpotato=100 plantain=80 butter=12 gravy=35')
put([52,113,191],'conch=60 potato=60 carrot=35 broth=150 oil=5','One assumed bowl of broth-based conch chowder','USDA cooked conch proxy; no cream assumed.')
put(57,'veal=190 grits=150 bluecheese=25 tomato=80 mushroom=40 oil=12')
put(58,'swordfish=180 tomato=100 olives=25 oil=15')
put(59,'friedchicken=180 salad=100 parmesan=20 dressing=20')
put([60,334],'lasagna=350','One assumed entrée portion, 230–525 g')
put(61,'gnocchi=230 pesto=40 parmesan=15 almonds=15','One assumed entrée','Almonds proxy pine nuts; pesto already contains oil.')
put(64,'prosciutto=70 mozzarella=70 salad=120 cream=30 tomato=40')
put(65,'salad=220 olives=30 dressing=30')
put(69,'bread=100 banana=70 chocsyrup=40 tahini=25 sugar=20','One assumed dessert calzone','Tahini proxies nut paste; filling recipe and dough/oil uptake unknown.')
put(70,'bread=100 ricotta=80 coconutcream=40 fruit=40 sugar=20','One assumed dessert calzone')
put(71,'salmon=180 teriyaki=35 sesameoil=5','One assumed salmon portion; no unlisted rice')
put(72,'pork=150 rice=160 broccoli=80 teriyaki=35')
put(73,'friedchicken=180 sweetsour=65','One assumed entrée without unlisted rice')
put(74,'friedshrimp=160 slaw=80 mayo=30')
put(78,'shumai=120 soy=15','Assumed four soup dumplings plus sauce','Steamed meat dumpling proxy; soup-bao wrappers and filling can differ.')
put(79,'bao=60 chicken=60 salad=35 teriyaki=15 mayo=15','One assumed bao bun')
put(81,'salad=180 dressing=25 sesameoil=5')
put(82,'flank=180 tomato=70 corn=100 feta=25 oil=8')
put(83,'belly=120 rice=150 beans=80 tomato=50 oil=8')
put([84,154],'corntortilla=25 rawtuna=70 avocado=25 sourcream=15 oil=8 salad=20','One assumed tostada')
put(90,'watermelon=200 sugar=10','One assumed small fruit plate')

# Butch's. Steak ounces are menu labels, not verified cooked edible masses.
put(94,'cinnamonroll=140 egg=50 milk=40 butter=15 ricotta=35 banana=70 walnuts=20 syrup=25')
put(95,'pancake=180 chocsyrup=25 syrup=40 whipped=30')
put(96,'omelet=150 shrimp=70 butter=10 ricotta=35 hashbrown=100')
put(97,'muffin=65 egg=100 canadian=45 hollandaise=50','One assumed two-egg Benedict with Canadian bacon','Salmon/crab substitutions are not included; English muffin is used, not a sweet muffin.')
put(98,'flank=120/145/180 friedegg=100 hashbrown=120','One assumed plate; steak modeled at about 145 g cooked','The menu 6 oz steak may be pre-cook weight. Cooked edible weight is an explicit assumption.')
put(99,'friedegg=100 bacon=25 sausage=55 hashbrown=110 bread=50')
put(100,'muffin=65 friedegg=50 bacon=20 american=20 hashbrown=110')
put(101,'bread=80 avocado=80 feta=25 tomato=40','One assumed toast order; optional egg/salmon excluded')
put(102,'bagel=100 smokedsalmon=70 creamcheese=35 salad=75')
put(103,'yogurt=180 pineapple=80 quinoa=50 almonds=20 pecans=15 syrup=10','One assumed bowl','Almonds include a small seed-energy proxy; actual hemp/quinoa amounts unknown.')
put([104,186,440],'croissant=50 danish=45 sweetmuffin=45','One assumed basket containing three small pastries','Number and size are unverified; estimate is for the basket, not per pastry.')
put([105,187,484],'fruit=220','One assumed fruit plate; no syrup')
unavailable([106,126,127,188,189,190,262,331,441,442,501],'This row lists selectable sides, sauces, fish, cereal/juices or buffet choices. Quantities and selection are not fixed.')
put(107,'salad=150 crab=60 tomato=20 bacon=15 onionrings=25 bluecheesedressing=35')
put(108,'rawtuna=90 pineapple=40 cucumber=30 sweetpotato=40 oil=5')
put(109,'shrimp=110 mayo=25 mango=20 sweetsour=20')
put(110,'beef=100 salad=40 oil=8')
put(111,'lamb=100 syrup=25','One assumed starter, edible meat only; bones excluded')
put(112,'onionrings=250','One assumed whole blooming-onion starter; dipping sauce excluded','Onion rings proxy the battered onion. Sharing changes calories consumed.')
put(114,'salad=180 dressing=25')
put(115,'steak=90/120/155 butter=3/6/12','Half of one shared 14 oz bone-in steak; sides and sauces excluded','Assumed 240 g cooked edible meat from the full steak after bone/cooking loss, split between two. Not 14 oz per person.')
put(116,'steak=170/220/285 butter=3/8/15','One 10 oz menu steak; sides/sauces excluded','Assumed cooked edible weight spans pre-cook versus cooked menu-weight interpretations.')
put(117,'filet=105/135/175 butter=3/7/14','One 6 oz menu filet; sides/sauces excluded','Cooked edible weight is assumed, not measured.')
put(118,'ribeye=210/270/340 butter=3/8/15','One 12 oz menu ribeye; sides/sauces excluded','Fat eaten and cooking loss vary; the menu weight basis is unspecified.')
put(119,'porkchop=190/250/330 butter=3/8/15','One 14 oz bone-in pork chop; sides/sauces excluded','Edible weight excludes assumed bone/cooking loss.')
put(120,'hen=220/300/420 butter=5/10/20','One assumed Cornish hen, edible meat and skin only; bones excluded')
put(121,'bass=135/165/200 butter=3/8/15','One 7 oz menu branzino fillet; sides/sauces excluded','Generic sea bass is the species proxy; menu-weight basis unknown.')
put(122,'filet=90/115/145 shrimp=50 butter=20 mashed=130 broccoli=70')
put(123,'snapper=180 beans=100 salad=70 oil=18')
put(124,'pumpkin=180 bulgur=170 mushroom=60 oil=18 syrup=25','One assumed entrée','Cooked bulgur proxies cooked farro; fat added separately.')
put(125,'dumpling=200 pumpkin=80 butter=30','One assumed entrée','Plain dumplings proxy spinners; dough recipe unknown.')
put([128,294,376],'filet=90 fries=90 broccoli=50 gravy=15','One assumed child-size plate')
put([129,293],'chicken=95 mashed=90 carrot=50 gravy=20','One assumed child-size plate')
put(130,'salmon=95 mashed=90 creamedspinach=60 butter=12','One assumed child-size plate')
put(131,'banana=90 icecream=70 fritter=40 sugar=20 caramel=20','One assumed dessert','Plain fritter proxies the cinnamon donut; candy/tuile represented by sugar.')
put(132,'cream=65 egg=30 milk=30 sugar=25 fruit=30','One assumed dessert ramekin','Cream/egg/milk/sugar approximate rich custard; no resort recipe disclosed.')
put(133,'cheesecake=130 cookie=20 pineapple=50','One assumed dessert')
put(134,'brownie=80 icecream=70 coconut=15','One assumed dessert including ice cream')
unavailable([135,136,137,138,139,140,141],'This row combines selectable drinks or an unspecified mini/glass/bottle pour. A specific recipe and serving size are needed.')

# Brü: assumed pours in grams, never claimed as recipe disclosure or ABV.
put(142,'coffee=150 spirit=40 cream=25','One assumed spiked coffee','Spirit quantity/strength and cream are assumptions.')
put(143,'coffeeliqueur=30 spirit=30 coffee=120','One assumed spiked coffee')
put(144,'creamliqueur=45 espresso=60','One assumed spiked coffee')
put(145,'coffeeliqueur=30 spirit=30 espresso=60','One assumed spiked coffee')
put(146,'spirit=40 coffeeliqueur=25 coffee=60 liqueur=15','One assumed cocktail; ice excluded from component weights')
put(147,'spirit=40 liqueur=20 mango=50 lime=20 sugar=8','One assumed cocktail')
put(148,'spirit=30 liqueur=25 sparkling=75','One assumed cocktail')
put(149,'spirit=40 liqueur=20 soda=100 lime=20','One assumed cocktail','Sweetened soda proxies ginger beer.')
put(150,'spirit=35 liqueur=25 coconutwater=70 mango=40 lime=20','One assumed cocktail','Mango proxies passion-fruit juice; Aperol represented by a generic liqueur.')
put(151,'sparkling=120 sugar=15','One assumed cocktail')
put(152,'spirit=50 sugar=8','One assumed rum old fashioned; no extra float')
put(153,'spirit=45 lime=25 sugar=15','One assumed daiquiri')

# Arizona's.
put(155,'avocado=100 bacon=15 chips=45 salad=40')
put(156,'tortilla=40 pork=50 oil=8 sourcream=15 avocado=20 tomato=20','One assumed taquito starter')
put(157,'shrimp=100 salad=60 lime=20 plantain=60')
put(158,'beans=100 broth=140 cream=20 feta=15 tomato=25','One assumed soup bowl')
put(159,'salad=180 coconutmilk=25 dressing=25')
put(160,'salad=160 bread=25 avocado=35 caesardressing=30')
put(161,'ribs=220 bbq=50 corn=120','One assumed entrée; edible rib meat only, bones excluded')
put(162,'tbone=230 corn=120 butter=20 parmesan=15 bakedpotato=200 sourcream=35','One assumed entrée; edible steak weight, bones excluded')
put(163,'tortilla=60 shrimp=130 tomato=60 corn=40 avocado=45 sourcream=25','Assumed two tacos with accompaniments')
put(164,'pork=130 beans=80 sweetpotato=90 rice=130 corn=40 cream=25 oil=10')
put(165,'whitefish=180 rice=160 broccoli=80 tomato=70 oil=10')
put(166,'patty=160 bun=75 salad=60 mayo=25','One assumed burger; no unlisted fries')
put(167,'lentils=180 tomato=80 corn=60 avocado=50 chips=40 oil=8')
put(168,'ribs=110 slaw=60 corn=80','One assumed child-size plate; rib bones excluded')
put(169,'chickenleg=90 bbq=20 fries=90','One assumed child-size plate; chicken bone excluded')
put(170,'mac=160 tomato=30','One assumed child-size bowl')
put(171,'tortilla=45 cheddar=45 butter=5','One assumed child-size quesadilla')
put(172,'chocpudding=140 cream=35 chocolate=20','One assumed mousse dessert','Pudding, cream and chocolate approximate mousse; recipe unknown.')
put(173,'flan=140','One assumed flan dessert')
put(174,'lemontart=120 mango=40','One assumed dessert','Lemon tart is a proxy for a mango-lime tart.')

# Schooners breakfast and dinner.
put(175,'friedfish=140 hashbrown=100 fritter=60','One assumed breakfast plate','Plain fried dough proxies festival.')
put(176,'omelet=150 shrimp=60 salad=50 avocado=40 prosciutto=20 cheddar=25')
put(177,'frenchtoast=150 banana=60 chocolate=25 pecans=20','One assumed breakfast plate','Chocolate plus nuts approximate Nutella topping; not a label match.')
unavailable(178,'This row offers chocolate-chip, blueberry or vanilla pancakes. Select a flavor and number of pancakes first.')
put(179,'muffin=65 egg=100 smokedsalmon=60 hollandaise=50')
put([180,434],'steak=140 friedegg=100 hashbrown=120')
put([181,435],'friedegg=100 hashbrown=110 bacon=25','One assumed breakfast with bacon','Ham/sausage choices require a different component amount.')
put(182,'veganlink=100 bakedbeans=140 tomato=80 hashbrown=110','One assumed vegan breakfast','Generic meatless breakfast links proxy the plant-based jerk pork.')
put(183,'bread=80 smokedsalmon=70 avocado=70 salad=20')
put(184,'yogurt=180 quinoa=50 fruit=100 pecans=15 almonds=15 coconut=12')
put(185,'oatmeal=200 sugar=15 fruit=40 almonds=20')
put(192,'crabcake=100 slaw=50 mango=30')
put(193,'scallops=90 creamedspinach=50 bacon=15 grits=80 butter=8','One assumed starter','Creamed spinach proxies creamed Brussels sprouts.')
put(194,'mussels=120 cream=60 butter=8','One assumed mussel starter; shells excluded')
put(195,'shrimp=90 salad=150 dressing=30')
put(196,'salad=130 fruit=60 beans=40 parmesan=20 dressing=25','One assumed salad','Beans approximate roasted chickpeas; no measured roasting loss.')
put(197,'broccoli=120 carrot=80 yogurt=40 oil=12 almonds=12','One assumed salad','Almonds proxy hemp seeds.')
put(198,'snapper=180 coconutmilk=80 mussels=60 corn=50 broccoli=60 pasta=120 oil=8')
put(199,'swordfish=180 carrot=100 sweetpotato=80 yogurt=45 oil=12 salad=40')
put(200,'tuna=180 cauliflower=90 carrot=50 broccoli=90 butter=15 dressing=20')
put(201,'ribeye=230 broccoli=80 mashed=140 creamcheese=25 gravy=35 onionrings=25')
put(202,'chicken=150 mushroom=70 pasta=220 alfredo=100 parmesan=20')
put(203,'eggplant=180 veganlink=100 rice=100 tomato=80 oil=15')
put(204,'cauliflower=200 veganlink=90 quinoa=100 broccoli=70 coconutmilk=70 oil=10')
put([205,472],'pasta=150 tomato=70 parmesan=12','One assumed child-size pasta bowl')
put([206,312],'nuggets=100 fries=90','One assumed child-size plate')
put(207,'friedfish=110 fries=90 mayo=20','One assumed child-size plate')
put(208,'lemontart=120 pineapple=40 meringue=10','One assumed dessert')
put(209,'choccake=110 fruit=40','One assumed dessert','Chocolate cake proxy; a flourless recipe may differ.')
put(210,'shortcake=120 ricotta=35 syrup=10 fruit=45','One assumed dessert','Ricotta and cream in shortcake proxy mascarpone topping.')

# Sapodilla's.
put(211,'conch=60 friedfish=70 bread=15 oil=8 salad=40 mayo=20','One assumed starter','Fried fish proxies fried calamari; coating/oil added only for the conch component.')
put(212,'snapper=80 coconutmilk=40 pineapple=35 lime=15 oil=6','One assumed starter','Cooked snapper profile proxies raw carpaccio.')
put(213,'pumpkin=130 coconutmilk=60 broth=100 bread=25 cashews=15 oil=8','One assumed starter soup','Pumpkin proxies butternut squash.')
put(214,'shrimp=90 pasta=100 salad=75 dressing=25 chips=15','One assumed starter','Tortilla chips proxy wonton crunch.')
put(215,'salad=150 fruit=60 ricotta=40 dressing=25')
put(216,'salad=100 fruit=80 bluecheese=30 almonds=20 sugar=10 dressing=25')
put(217,'veganlink=80 lentilsoup=180 syrup=15','One assumed starter')
put(218,'lobster=180 watermelon=60 salad=100 corn=100 cream=25 oil=12','One assumed lobster entrée; edible tail meat only')
put(219,'snapper=200 salad=160 pumpkin=70 coconutmilk=70 oil=10')
put(220,'whitefish=180 shrimp=60 tomato=80 sweetmash=150 broccoli=70 oil=10','One assumed entrée','Generic white fish proxies grouper.')
put(221,'filet=180 pate=30 mashed=140 cream=25 broccoli=50 gravy=35','One assumed entrée','Pâté proxies foie gras; mashed potato plus cream proxies creamed cassava.')
put(222,'lamb=200 fries=130 salad=100 gravy=35','One assumed entrée; edible lamb only, bones excluded')
put(223,'couscous=180 salad=140 paneer=70 coconutmilk=70 almonds=20 oil=8','One assumed vegetarian entrée; optional chicken excluded')
put(224,'veganchicken=170 sweetmash=150 spinach=70 carrot=60 gravy=35')
put(225,'nutpie=120 banana=50 cookie=15','One assumed dessert','Nut pie proxies banana-hazelnut tart; alcohol retention not known.')
put(226,'custard=130 coconutmilk=25 pineapple=40 mango=30 sugar=8','One assumed dessert')
put(227,'choccake=110 icecream=65','One assumed dessert')
put(228,'yogurt=150 ricotta=40 fruit=50 sugar=10','One assumed parfait dessert','Ricotta proxies mascarpone; actual fat content varies.')

# Bella Napoli, explicit whole individual pizza serving assumption.
put(229,'pizza=330 conch=70 salad=40','One assumed whole individual pizza; not per slice')
put(230,'pizza=330 chicken=70 mango=50','One assumed whole individual pizza; not per slice')
put(233,'pepperonipizza=350','One assumed whole individual pizza; not per slice')
put(235,'pizza=330 ham=60 pineapple=60','One assumed whole individual pizza; not per slice')
put(236,'pizza=330 chicken=70 gouda=30 bbq=35','One assumed whole individual pizza; not per slice')
put(237,'pizza=330 alfredo=40 prosciutto=50 mushroom=50 spinach=25','One assumed whole individual pizza; not per slice')
put(238,'pizza=330 olives=35 tuna=20 tomato=40','One assumed whole individual pizza; not per slice','Tuna proxies anchovy calories; fish quantity is assumed.')
put(239,'vegpizza=350 olives=25','One assumed whole individual pizza; not per slice')
put(240,'pizza=330 creamcheese=45 parmesan=20 oil=10','One assumed whole individual pizza; not per slice')
put(241,'bread=160 mozzarella=80 sausage=50 tomato=70 oil=10','One assumed whole calzone','Sausage proxies pepperoni.')
put(242,'bread=100 butter=25 tomato=50','One assumed order of pizza bites')
put(243,'bread=120 chocsyrup=50 banana=80 butter=10','One assumed dessert calzone')

# Kimonos is a multi-course meal: grill entries are components, not a full dinner.
put(244,'crab=30 mayo=10 shrimp=35 pasta=45 shumai=40 soy=10','One assumed appetizer sampler')
put(245,'coconutmilk=70 tofu=50 mushroom=40 broth=130','One assumed soup bowl')
put(246,'salad=160 dressing=25','One assumed starter salad')
put(247,'steak=110 oil=8 teriyaki=25','One assumed teppanyaki beef portion only; soup, salad, rice and other proteins separate')
put(248,'chicken=110 oil=8 teriyaki=25','One assumed teppanyaki chicken portion only; soup, salad, rice and other proteins separate')
put(249,'shrimp=110 oil=8 teriyaki=25','One assumed teppanyaki shrimp portion only; soup, salad, rice and other proteins separate')
put(250,'whitefish=110 oil=8 teriyaki=25','One assumed teppanyaki fish portion only; soup, salad, rice and other proteins separate','Generic white fish proxies mahi-mahi.')
put(251,'friedrice=150','One assumed teppanyaki rice serving, separate from proteins')
put(252,'pasta=180 salad=100 teriyaki=35 oil=12','One assumed noodle entrée')
put(253,'tofu=150 salad=150 oil=15 soy=20','One assumed tofu entrée')
put(254,'icecream=110','Three assumed small scoops, about 110 g total','Vanilla profile proxies the three flavors; serving weight not observed.')

# Soy: roll portions match the menu's four pieces, not an eight-piece roll.
put(256,'rawtuna=80 seaweed=50 soy=20 oil=5','One assumed starter')
put(257,'rawsalmon=85 dressing=15 lime=15','One assumed starter')
put(258,'rawtuna=50 rawsalmon=50 chips=30 soy=15','One assumed starter','Tortilla chips proxy wonton chips.')
put(259,'seaweed=90 sesameoil=5 soy=10','One assumed seaweed-salad side')
put(260,'edamame=90','One assumed order, shelled beans only; pods excluded')
put(261,'misosoup=220','One assumed small soup bowl')
put(263,'rice=90 friedshrimp=40 rawtuna=30 seaweed=2 soy=15','Four pieces, as listed; assumed rice/filling weights')
put(264,'rice=90 friedshrimp=45 mayo=20 avocado=25 chips=10 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(265,'rice=90 rawtuna=30 crab=30 mayo=18 teriyaki=15 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(266,'rice=90 crab=25 shrimp=30 avocado=25 cucumber=20 chips=12 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(267,'rice=90 rawtuna=40 cucumber=20 mayo=12 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(268,'rice=90 crab=25 avocado=20 cucumber=20 smokedsalmon=30 mayo=15 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(269,'rice=90 crab=35 cucumber=20 avocado=30 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(270,'rice=90 creamcheese=35 cucumber=20 sesameoil=3 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(271,'rice=90 salad=50 avocado=30 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
put(272,'rice=90 avocado=50 seaweed=2','Four pieces, as listed; assumed rice/filling weights')
unavailable(273,'This row groups salmon, tuna and yellowtail rolls. Select the fish first; the menu serving is four pieces.')
put(274,'rice=180 crab=40 cucumber=40 avocado=45 rawsalmon=40 rawtuna=60 seaweed=5','One assumed sushi bowl','Tuna proxies yellowtail; masago represented by a small seafood allowance.')
put(275,'rice=180 crab=40 cucumber=40 avocado=45 eel=60 teriyaki=25','One assumed sushi bowl')
put(276,'rice=180 rawtuna=90 chips=25 teriyaki=25 mayo=25','One assumed sushi bowl')

# Le Petit Chateau.
put(277,'onion=100 broth=180 bread=40 gruyere=30 butter=10','One assumed soup bowl')
put(278,'scallops=100 cream=40 gruyere=20 mushroom=40 bread=15 butter=8','One assumed starter')
put(279,'rawtuna=90 olives=20 fries=35 broccoli=40 egg=50 salad=100 dressing=25')
put(280,'shrimp=90 quinoa=100 onionrings=15 dressing=25','One assumed starter')
put(281,'salad=150 fruit=75 dressing=30')
put(282,'duck=180 mushroom=70 spinach=30 fruit=65 gravy=35 oil=8')
put(283,'filet=180 pate=35 scalloped=160 gravy=40')
put(284,'lamb=200 tomato=70 eggplant=70 potato=130 oil=15 gravy=35','One assumed entrée; edible lamb only, bones excluded')
put(285,'whitefish=180 cream=60 seafoodsoup=100 broccoli=80 butter=10','One assumed entrée','Generic white fish proxies corvina; seafood soup proxies bisque.')
put(286,'shrimp=180 tomato=100 olives=25 grits=150 bluecheese=20 oil=12')
put(287,'friedchicken=170 ham=35 gruyere=35 salad=120 gravy=35')
put(288,'puff=80 onion=70 goatcheese=50 tomato=80 eggplant=90 oil=10')
put(289,'veggiepatty=170 mushroom=100 broccoli=80 dressing=25 oil=10','One assumed entrée','Plant-based patty proxies soy mince; no product disclosure found in the saved menu.')
put(290,'choccake=110 cream=35 fruit=40','One assumed dessert')
put(291,'cream=65 egg=30 milk=30 sugar=25 cookie=25 pineapple=40','One assumed dessert','Cream/egg/sugar approximate rich custard; cookie proxies financier; alcohol retention unknown.')
put(292,'custard=100 cake=60 fruit=50','One assumed dessert','Custard plus sponge cake proxy clafoutis.')
put(295,'friedshrimp=90 rice=100 corn=70 sweetsour=20','One assumed child-size plate')
put(296,'croissant=55','One assumed plain croissant')
unavailable(297,'The guest report gives no size, filling or count for macarons. No defensible item-matched portion is available.')
put(298,'eclair=85','One assumed chocolate éclair')
unavailable(299,'This guest-reported row combines different coffees, syrups and temperatures. Choose a drink and cup size first.')

# Bobby Dee's: burgers are separate from selectable side orders.
put(300,'patty=170 bun=75 american=35 salad=40 mayo=25','One assumed double burger; no unlisted fries')
put(301,'patty=150 bun=75 bacon=25 mushroom=40 onion=30 swiss=30 mayo=15','One assumed burger; no unlisted fries')
put(302,'patty=150 bun=75 bbq=30 onionrings=30 american=30 salad=40','One assumed burger; no unlisted fries')
put(303,'chicken=150 bun=75 mayo=25 salad=30','One assumed chicken burger; no unlisted fries')
put(304,'friedfish=150 bun=75 slaw=50 bbq=25','One assumed fish burger; no unlisted fries')
put(305,'veggiepatty=130 bun=75 tomato=40 avocado=40','One assumed veggie burger; no unlisted fries')
put(306,'bread=120 ribeye=140 provolone=40 onion=70 oil=8','One assumed sandwich; no unlisted sides')
put(307,'hotdog=70 dogbun=55 beef=45 beans=30 cheddar=25 tomato=25','One assumed chili-cheese dog')
put(308,'hotdog=70 dogbun=55','One assumed plain hot dog on a bun')
unavailable(309,'Wing count, edible weight and sauce choice are unspecified. A serving and sauce selection are needed.')
put(310,'tortilla=65 sausage=45 mozzarella=50 tomato=50 oil=5','One assumed pizzadilla','Sausage proxies pepperoni.')
put(311,'wheatbread=70 tuna=85 mayo=25','One assumed tuna salad sandwich')
put(313,'bread=60 american=35 butter=12','One assumed small grilled-cheese sandwich')
put(314,'mac=160','One assumed small mac-and-cheese side')
put(315,'mac=140 beef=35 beans=30 tomato=25','One assumed small chili-mac side')
put(316,'beef=45 beans=60 tomato=60 chips=40','One assumed small chili-and-chips side')
put(317,'fries=100','One assumed side order')
put(318,'hummus=65','One assumed side, no unlisted pita')
put(319,'carrot=60 celery=60','One assumed raw vegetable side')
put(320,'peas=65 carrot=65 butter=8','One assumed side')
put(321,'fruit=130','One assumed fruit cup')

# Mr. Mac: hypothetical truck cups, based on guest names only.
put(322,'mac=220','One assumed truck cup, about 145–330 g','Guest-reported dish; cup size and recipe not verified.')
put(323,'mac=220 lobster=60','One assumed truck cup','Guest-reported dish; cup size and recipe not verified.')
put(324,'mac=220 crab=60','One assumed truck cup','Guest-reported dish; cup size and recipe not verified.')
put([325,326],'mac=220 chicken=65 bbq=20','One assumed truck cup','Guest-reported dish. Generic sauce proxies jerk/Buffalo sauce; exact product unknown.')
put(327,'mac=220 pork=65 bbq=20','One assumed truck cup','Guest-reported dish; portion not verified.')
put(328,'mac=220 beef=65','One assumed truck cup','Guest-reported dish; portion not verified.')
put(329,'mac=220 tomato=40 avocado=40','One assumed truck cup','Guest-reported dish; portion not verified.')
put(330,'mac=100 bread=20 oil=12','Assumed three fried mac-and-cheese balls','Guest report; piece count, coating and retained oil are assumptions.')

# Mario's.
put(332,'veal=190 grits=180 oil=12 gravy=40')
put(333,'veal=200 pumpkin=140 salad=100 butter=15 gravy=35')
put(335,'pasta=220 octopus=100 tomato=90 parmesan=15 almonds=15 oil=12')
put(336,'pasta=220 shrimp=140 tomato=60 cream=70 butter=12')
put(337,'pasta=220 sausage=90 spinach=50 cream=60 parmesan=15 butter=8')
put(338,'salmon=180 spinach=80 sausage=50 beans=90 cream=45 oil=10')
put(339,'friedchicken=180 pasta=160 tomato=100 mozzarella=35')
put(340,'rice=200 peas=70 parmesan=25 butter=20 cream=35')
put(341,'pasta=220 tomato=120 mozzarella=60 oil=12')
put(342,'lentils=100 salad=70 pasta=200 olives=25 tomato=90 oil=15')
put(343,'chicken=90 alfredo=35 mashed=90 salad=65','One assumed child-size plate')
put(344,'pasta=140 beef=60 tomato=70 parmesan=10','One assumed child-size plate')
put(345,'salmon=90 potato=90 butter=12 broccoli=45 carrot=35','One assumed child-size plate')
put(346,'cake=50 ricotta=70 cream=35 sugar=15 coffee=15','One assumed tiramisù','Sponge/ricotta/cream proxies sponge and mascarpone; alcohol retention unknown.')
put(347,'nutpie=120 ricotta=40 fruit=30','One assumed nut-tart dessert','Pecan pie proxies the pistachio/almond tart; nuts and dried-fruit proportions unknown.')
put(348,'choctart=120 chocsyrup=25 icecream=60','One assumed dessert')

# Dino's.
same(351,233)
put(352,'pizza=350 mozzarella=30 gruyere=25 parmesan=20 alfredo=40','One assumed whole individual pizza; not per slice','Extra cheese/cream sauce represent the richer four-cheese topping.')
put(353,'pizza=330 alfredo=45 mushroom=60 salad=20','One assumed whole individual pizza; not per slice')
put(354,'vegpizza=350','One assumed whole individual pizza; not per slice')
put(356,'pizza=330 chicken=80 pesto=35 parmesan=20','One assumed whole individual pizza; not per slice')
put(357,'patty=180 bun=80 onion=40 mushroom=40 provolone=35 creamcheese=20 mayo=20','One assumed double burger; no unlisted fries')
put(358,'friedchicken=160 bread=120 mayo=30 salad=50','One assumed sandwich; no unlisted side')
put(359,'beef=150 bread=120 parmesan=35 tomato=60','One assumed meatball sandwich; no unlisted side')
put(360,'focaccia=130 olives=30 mushroom=60 salad=90 pesto=30 mozzarella=50','One assumed sandwich; no unlisted side')
put(361,'salad=160 bacon=20 tomato=40 parmesan=25 bread=35 caesardressing=30')
put(362,'salad=160 bread=70 dressing=30')

# Cricketer's: selectable handheld sides excluded instead of silently choosing fries.
put(363,'spinach=60 creamcheese=60 cheddar=30 salad=40 pita=70','One assumed dip-and-pita starter','Mixed salad vegetables proxy artichoke.')
put(364,'cauliflower=140 cream=40 broth=130 oil=8','One assumed soup bowl')
put(365,'salad=150 peas=40 cucumber=50 dressing=25 syrup=8')
put(366,'friedfish=190 fries=160 peas=80 mayo=30','One assumed adult pub plate')
put(367,'chickenleg=180 broccoli=80 rice=140 syrup=25 yogurt=45 naan=80 oil=10','One assumed adult pub plate; bone excluded')
put(368,'chicken=130 salad=100 fruit=45 puff=90 butter=10 gravy=50','One assumed individual chicken pie','Prepared puff pastry plus filling; no unlisted side.')
put(369,'lentils=140 beans=90 salad=100 mashed=180 parmesan=25 oil=10')
put(370,'wings=180 bluecheesedressing=35 carrot=40 celery=40 fries=130 bbq=30','One assumed pub plate; wing bones excluded','Generic sauce proxy, not measured Buffalo recipe.')
put(371,'bread=120 shortrib=130 gruyere=40 onion=40 mayo=25 gravy=40','One assumed handheld only; choice of salad/fries excluded','Gruyère proxies havarti.')
put(372,'patty=160 bun=80 bacon=25 mushroom=40 swiss=35','One assumed burger only; choice of salad/fries excluded')
put(373,'veggiepatty=140 bun=80 mayo=25 provolone=30','One assumed burger only; choice of salad/fries excluded')
put(374,'sausage=100 fritter=70 mayo=20 tomato=25','One assumed corn dog only; choice of salad/fries excluded','Fried-dough proxy represents the corn coating.')
put(375,'patty=85 bun=55 american=20 fries=90','One assumed child-size plate')
put(377,'chicken=95 bbq=20 rice=100 broccoli=60','One assumed child-size plate')
put(378,'carrot=60 celery=60 pita=45 hummus=50','One assumed child-size plate')
put(379,'cake=100 dates=35 butter=15 caramel=35 icecream=60','One assumed dessert','Sponge cake with dates approximates sticky date pudding.')
put(380,'cherrypie=130 cookie=25 icecream=65','One assumed dessert')

# Barefoot by the Sea.
put(382,'whitefish=120 tortilla=65 corn=45 tomato=50 slaw=50','Assumed two fish tacos')
put(383,'whitefish=150 salad=160 tomato=30 bread=30 caesardressing=35')
put(384,'friedfish=150 bun=80 mayo=25 salad=40 fries=120')
put(385,'cucumber=140 yogurt=65 broth=80 shrimp=70 oil=5','One assumed soup with shrimp skewer')
put(386,'pork=140 bun=80 bbq=35 pineapple=40 slaw=60 fries=120')
put(387,'chicken=100 mayo=30 fruit=30 bacon=25 bun=80','One assumed club sandwich only; choice of greens/fries excluded')
put(388,'chickenleg=200 fries=120 slaw=70 gravy=35','One assumed entrée; bone excluded')
put(389,'veganchicken=140 salad=190 avocado=60 coconutmilk=30 dressing=25')
put(390,'beans=100 veggiepatty=80 salad=160 avocado=50 tomato=60 tortilla=65 oil=10')
put(391,'wheatbread=60 tuna=70 cheddar=25 mayo=15 cucumber=60','One assumed child-size plate')
put(392,'pasta=140 chicken=75 broccoli=65 butter=12','One assumed child-size plate','Butter is an explicit cooking-fat assumption; sauce not disclosed.')
put(393,'tortilla=50 ham=55 cheddar=25 salad=60','One assumed child-size plate')
put(394,'applepie=150','One assumed pie slice')
put(395,'brownie=100','One assumed brownie; no unlisted ice cream')
put(396,'fritter=90 conch=30 mayo=25','Assumed three small fritters with aioli','Count and conch content are assumptions.')
put(397,'friedshrimp=110 coconut=15 sweetsour=25 mango=20','One assumed starter')
put(398,'crabcake=110 mayo=20 salad=30','One assumed starter')
put(399,'seafoodsoup=230 cream=35 bread=120','One assumed seafood chowder in an edible bread bowl')
put(400,'belly=90 plantain=60 mango=30 avocado=30 oil=6','One assumed starter')
put(401,'salad=150 beans=50 quinoa=65 mango=50 dressing=25')
put(402,'whitefish=180 corn=110 cream=25 plantain=90 avocado=45 salad=35 oil=10')
put(403,'friedfish=170 coconut=20 salad=130 pumpkin=60 rice=150 broth=80')
put(404,'shrimp=100 steak=170 mashed=150 gravy=40 salad=25')
put(405,'ribs=220 potato=100 mayo=25 fritter=65 slaw=70 bbq=40','One assumed entrée; rib bones excluded')
put(406,'veggiepatty=150 bun=80 pineapple=40 sweetfries=130 mayo=25')
put(407,'mac=170 broccoli=55 slaw=55','One assumed child-size plate')
put(408,'nuggets=110 fries=90 mayo=15 syrup=10','One assumed child-size plate','Mayo and syrup proxy honey mustard.')
put(409,'beef=95 teriyaki=25 broccoli=60 rice=100','One assumed child-size plate')
put(410,'cheesecake=130 mango=35 cookie=20 chocolate=15','One assumed dessert','Generic chocolate proxies white chocolate energy.')
put(411,'lemontart=120 fruit=30 whipped=25','One assumed dessert')
put(412,'choctart=120 banana=45 chocolate=20 cookie=15','One assumed dessert')

# Jojo Java, each cup size/milk choice is hypothetical.
put(413,'espresso=30/45/60','One single/double espresso; no milk or sugar')
put(414,'espresso=60 condensed=35','One assumed double espresso with condensed milk')
put(415,'espresso=60 tonic=180','One assumed espresso tonic; ice excluded')
put(416,'espresso=60 milk=200','One assumed small/medium whole-milk latte, unsweetened')
put(417,'espresso=45 milk=100','One assumed small whole-milk cappuccino, unsweetened')
put(418,'espresso=60 milk=150','One assumed whole-milk flat white, unsweetened')
put(419,'espresso=45 milk=25','One assumed macchiato; milk amount uncertain')
put(420,'espresso=45','One assumed Americano; water has no calories, additions excluded')
put(421,'espresso=45 milk=120 chocsyrup=30','One assumed mochaccino')
put(422,'coffee=240','One assumed 240 mL black coffee; additions excluded')
put(423,'coffee=120 milk=120','One assumed café au lait, unsweetened')
put(424,'coffee=80 milk=180','One assumed iced latte; ice and added sugar excluded')
put(425,'coffee=100 tonic=170','One assumed cold-brew tonic; ice excluded')
unavailable(426,'This row groups iced latte, Americano and tea, with substantially different calories. Choose one drink and size first.')
put(427,'milk=220 chocsyrup=40','One assumed hot/iced chocolate; ice excluded, no whipped cream')
put([428,522],'milk=100 chocsyrup=15 marshmallow=10','One assumed small babyccino; about 125 g before foam')

# Neptune's breakfast.
put(429,'muffin=65 egg=100 ham=50 hollandaise=50')
put(430,'bread=80 avocado=70 tomato=35 feta=25 egg=50 hollandaise=30')
put(431,'frenchtoast=160 banana=70 fruit=40 syrup=45','One assumed breakfast plate','Syrup modeled without an assumed retained alcohol amount.')
put(432,'pancake=170 fruit=45 syrup=40')
put(433,'omelet=160 parmesan=20 provolone=25 salad=80 prosciutto=25 sourcream=25')
put(436,'veganlink=100 bakedbeans=150 salad=80 hashbrown=110')
put(437,'yogurt=180 fruit=90 granola=55 syrup=15')
put(438,'fruit=220 syrup=25')
put(439,'oatmeal=200 sugar=15 raisins=20 almonds=20')
put(443,'friedfish=180 yogurt=50','One assumed fried-fish basket; no unlisted fries')
put(444,'shrimp=100 bread=80 tomato=65 pesto=20','One assumed bruschetta order')
put(445,'whitefish=180 salad=150 cream=40 butter=15 oil=8')
put(446,'salmon=170 quinoa=140 fruit=45 salad=70 oil=12')
put(447,'chicken=160 pita=80 salad=70 yogurt=50 oil=8')
put(448,'salad=200 olives=30 feta=60 pita=60 dressing=25','One assumed base Greek salad; optional chicken/shrimp excluded')
put(449,'salad=220 pita=60 oil=12 dressing=25','One assumed base fattoush; optional chicken/shrimp excluded')
put(450,'lentilsoup=200 bread=90 ham=50 cheddar=35 butter=12 onionrings=80')
put(451,'patty=160 bun=80 cheddar=30 fries=120','One assumed burger with cheddar and fries','Other cheese choices vary.')
put(452,'veggiepatty=140 bun=80 tomato=45 syrup=10 fries=120')
put(453,'patty=85 bun=55 mayo=15 fries=90','One assumed child-size plate')
put(454,'pita=55 peanutbutter=30 fruit=50 carrot=40 cucumber=40','One assumed child-size plate')
put(455,'churro=85 banana=50 cream=25 chocsyrup=30','One assumed dessert')
put(456,'fritter=75 sugar=10 fruit=30 whipped=30','One assumed filled doughnut dessert','Fried dough plus fruit/sugar proxies jam-filled doughnut.')
put(457,'pineapple=180 sugar=20','One assumed fruit dessert')
put(458,'seafoodsoup=200 coconutmilk=40 shrimp=40 mussels=35 whitefish=35','One assumed starter bisque')
put(459,'octopus=100 tomato=80 olives=25 bread=40 oil=10','One assumed starter')
put(460,'mussels=110 cream=45 onion=35 bread=40 butter=8','One assumed mussel starter; shells excluded')
put(461,'carrot=120 feta=50 walnuts=25 sugar=12 fruit=40 oil=8')
put(462,'beet=140 yogurt=45 salad=70 almonds=20 oil=8','One assumed starter salad','Almonds proxy hemp-seed dukkah.')
put(463,'fruit=160 salad=70 oil=12 lime=15','One assumed starter salad')
put(464,'bass=230 tomato=90 olives=30 beans=60 oil=20','One assumed whole-fish entrée; edible fish flesh only, no bones','Generic sea bass proxies branzino; whole served mass is larger than edible mass.')
put(465,'swordfish=180 peas=130 tomato=70 butter=25 cream=20')
put(466,'lamb=210 mashed=130 broccoli=90 oil=12 gravy=40','One assumed lamb-shank entrée; bones excluded','Mashed potato proxies parsnip purée.')
put(467,'chickenleg=190 beans=140 plantainchips=30 salad=60 oil=12')
put(468,'clams=100 sausage=90 pasta=220 butter=25 dressing=20')
put(469,'bulgur=220 pumpkin=140 butter=25 pistachio=25 parmesan=15','One assumed entrée','Bulgur proxies cooked farro; risotto-style additions modeled separately.')
put(470,'friedfish=110 peas=80 mayo=20','One assumed child-size plate')
put(471,'chicken=100 potato=100 oil=8 broccoli=60','One assumed child-size plate')
put(473,'cheesecake=120 nutpie=40 fruit=35 syrup=15','One assumed dessert','Nut pie proxies honeyed nuts/phyllo topping.')
put(474,'eclair=90 meringue=15','One assumed dessert','Generic filled éclair proxies lemon éclair.')
put(475,'cake=100 oil=12 pineapple=50','One assumed dessert','Sponge cake plus olive oil proxies olive-oil cake.')

# Sky.
put(476,'frenchtoast=160 fruit=70 caramel=35 custard=45')
put(477,'waffle=130 smokedsalmon=70 sourcream=30 egg=50')
put(478,'corntortilla=35 tomato=60 avocado=50 friedegg=50 sugar=8 oil=5','One assumed egg tostada')
put(479,'bread=80 avocado=70 bacon=20 egg=50 tomato=40')
put(480,'pancake=160 banana=65 oats=20 syrup=40')
put(481,'pancake=180 whipped=30 syrup=45')
put(482,'friedegg=100 bacon=25 sausage=55 hashbrown=110 tomato=80')
put(483,'greek=180 fruit=100 coconut=15 granola=50')
put(485,'scallops=90 lime=25 celery=30 salad=20','One assumed ceviche starter','Cooked scallop proxy for citrus-marinated scallops.')
put(486,'rawtuna=90 avocado=40 salad=40 chips=25 dressing=15')
put(487,'mussels=50 shrimp=50 clams=45 tomato=100 broth=100 oil=8','One assumed seafood-stew starter')
put(488,'belly=100 sweetmash=80 bbq=30 salad=25','One assumed starter')
put(489,'salad=100 quinoa=100 watermelon=70 almonds=20 dressing=25')
put(490,'rice=200 mussels=50 shrimp=60 octopus=70 avocado=60 cream=20 oil=12','One assumed seafood-rice entrée','Octopus proxies squid as well as octopus; shell weights excluded.')
put(491,'whitefish=180 quinoa=140 corn=60 onion=70 cream=30 oil=15')
put(492,'salmon=180 mashed=150 mango=40 tomato=40 spinach=50 butter=12','One assumed entrée','Mashed potato proxies cassava purée.')
put(493,'duck=180 mushroom=80 broccoli=60 carrot=100 butter=12 syrup=20')
put(494,'filet=180 hashbrown=140 teriyaki=30 broccoli=60 carrot=50 butter=10')
put(495,'puff=85 creamedspinach=130 cashews=30 tofu=60 tomato=90 almonds=15','One assumed börek entrée','Puff pastry proxies börek pastry; tofu/cashew filling and portion unmeasured.')
put(496,'meringue=45 whipped=55 fruit=100','One assumed pavlova dessert')
put(497,'choccheesecake=110 brownie=45 cookie=20','One assumed layered dessert')
put(498,'chickenleg=180 bbq=20','One assumed jerk-chicken order; bones and separately listed sides excluded','Guest report only; edible meat and skin weight hypothetical.')
put(499,'pork=170 bbq=20','One assumed jerk-pork order; separately listed sides excluded','Guest report only; edible portion hypothetical.')
put(500,'whitefish=180 oil=10','One assumed grilled-fish order; separately listed sides excluded','Guest report only; species and portion unknown, generic cooked white fish proxy.')

# General bars/drinks lists. Recipe conflicts are withheld rather than guessed.
unavailable([502,503,504,505,506,507,508,509,516,517,519,520,521,523,524,525,526,531],
 'Serving/pour or recipe is unspecified, this row groups alternatives, or the drink is identified only by a guest name. Choose a recipe and size before estimating.')
put(510,'coffee=240','One assumed 240 mL black coffee; milk/sugar excluded')
put(511,'spirit=28/30/34 liqueur=28/32/38 milk=75/90/105 sugar=6/10/15 banana=80/118/150 pineapple=10/20/35','One drink made to the published Beaches Dirty Banana ingredient list; ice excluded','Official blog specifies milk, crème de cacao and rum; the saved brief description says cream. Generic liqueur and rum profiles, banana size and syrup concentration remain assumed.')
unavailable(512,'The official Bob Marley blog lists rum but its blending steps do not specify where the rum is added; mix brands/concentration are unspecified. No fixed calorie estimate is assigned.')
unavailable(513,'The official Miami Vice recipe gives two rum pours but unspecified commercial daiquiri/colada mixes. Their concentrations and served yield need verification before estimating.')
put(514,'spirit=40/44/50 creamliqueur=40/46/55 liqueur=12/16/20 sugar=6/10/15 banana=80/118/150 fruit=3/5/10','One drink based on the published Beaches Hummingbird ingredient list; ice excluded','Generic spirit, rum-cream and cacao-liqueur profiles; grenadine modeled as sugar/water, banana size assumed.')
unavailable(515,'The official Purple Rain ingredient list names rum, while its instructions name gin, and splash sizes are unspecified. Recipe conflict must be resolved before estimating.')
put(518,'pineapplejuice=140 coconutcream=65 milk=40','One assumed virgin piña colada; ice excluded','No resort recipe/pour disclosed; coconut cream sweetness and serving size can change calories substantially.')
put(527,'spirit=40 pineapplejuice=110 sparkling=60','One assumed Caicos Sling; ice excluded','Older guest-reported ingredients; recipe/pour not verified.')
put(528,'spirit=40 sake=40 cranberry=60 pineapplejuice=60 sugar=8','One assumed Saki Cruise; ice excluded','Older guest report; vanilla vodka/sweetening approximated.')
put(529,'liqueur=45 soda=150 lime=20 fruit=30','One assumed Pimm’s Cup; ice excluded','Generic liqueur proxies Pimm’s; older guest report, strength and recipe not verified.')
put(530,'spirit=40 liqueur=25 orangejuice=100','One assumed Fuzzy Buccaneer; ice excluded','Generic liqueur proxies peach schnapps; older guest report.')
put(532,'coconutwater=250','One assumed 250 mL portion of coconut water; no coconut flesh','Actual coconut yield varies; not a calorie estimate for the whole coconut.')

if __name__ == '__main__':
    missing = set(range(len(ROWS))) - MODELS.keys()
    print('Assigned',len(MODELS),'of',len(ROWS),'Missing', sorted(missing))
