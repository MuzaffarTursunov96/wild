Skip to content
Search or jump to…
Pull requests
Issues
Codespaces
Marketplace
Explore
 
@MuzaffarTursunov96 
iBekzod
/
parsing
Private
Code
Issues
Pull requests
Actions
Projects
Security
Insights
parsing/parse_wild.py /
@iBekzod
iBekzod file added
Latest commit 39e7b6f on Nov 18, 2021
 History
 1 contributor
1054 lines (960 sloc)  48 KB

import random
import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests
import os
import ast
from slugify import slugify
import shutil
import json
from parse.models import AttributeCategory,AttributeTranslations,Attributes,BranchTranslations,Branches,BrandTranslations,Brands,Categories,CategoryTranslations,CharacteristicTranslations,Characteristics,ColorTranslations,Colors,ElementTranslations,Elements,Products,Uploads,VariationTranslations,Variations,BrandCategory
from django.core.management.base import BaseCommand
from jsondiff import diff
from django.core.exceptions import ObjectDoesNotExist
import argon2, binascii
from django.db.models import Q



class WildberiesParser:


    def check_exists(self,cate_name, prod_name):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{cate_name}\{prod_name}\product_detail.html')
        return filees

    def get_slugify(self,name):
        return slugify(f'{name}', to_lower=True)


    def nom(self,product_href):
        l = ''
        for i in reversed(product_href[:-25]):
            if i != '/':
                l += i
            else:
                break
            s = ''
            for i in reversed(l):
                s += i
        return s

    def prod_papka_yaratish(self,cate_name, nomi):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{cate_name}\{nomi}'):
            return True
        else:
            return False


    def cut_model(self,names,brand,diagonal):
        print(f'1-----------{names}------brand={brand}')
        # names=names
        if diagonal !='':
            rep_list=[f'{brand.capitalize()}',f'{brand.lower()}','Wi-Fi','LTE','+',f'{diagonal}','Cellular']
        else:
            rep_list = [f'{brand.capitalize()}',f'{brand.lower()}','Wi-Fi', 'LTE', '+','Cellular']
        a = names
        for rep in rep_list:
            if f'{rep}' in names:
                a=names.replace(rep,'')
                names=a

        # print(f'2---------{a}')
        if 'Gb' in names:
            gb_ind = names.index('Gb')
            h = ''
            for i in reversed(names[:gb_ind]):
                h += i
            pro_ind = h.index(' ')
            a = ''
            c = h[pro_ind:]
            for i in reversed(c):
                a += i
        elif "TB" in names:
            gb_ind = names.index('TB')
            if names[gb_ind+2]==' ':
                h = ''
                for i in reversed(names[:gb_ind]):
                    h += i
                pro_ind = h.index(' ')
                a = ''
                c = h[pro_ind:]
                for i in reversed(c):
                    a += i
        elif "GB" in names:
            gb_ind = names.index('GB')
            h = ''
            for i in reversed(names[:gb_ind]):
                h += i
            try:
                pro_ind = h.index(' ')
            except ValueError as ex:
                pro_ind=0
            a = ''
            c = h[pro_ind:]
            for i in reversed(c):
                a += i
        elif "Tb" in names:
            gb_ind = names.index('Tb')
            h = ''
            for i in reversed(names[:gb_ind]):
                h += i
            pro_ind = h.index(' ')
            a = ''
            c = h[pro_ind:]
            for i in reversed(c):
                a += i
        cy=a.split(';')[0]
        # print(f'3-----------{cy}')
        return cy

    def check_img_dir(self,category_name, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\{images}'):
            return True
        else:
            return False
    def branch_translation(self,branch_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=BranchTranslations(
                branch_id=branch_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()




    def brand_translation(self,brand_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=BrandTranslations(
                brand_id=brand_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()
    def color_translation(self,color_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=ColorTranslations(
                color_id=color_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()

    def var_translation(self,var_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            VariationTranslations(
                variation_id=var_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()
    def elem_translation(self,elem_id,name,des):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            ElementTranslations(
                element_id=elem_id,
                name=name,
                description=des,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()


    #######################        Baza       #############################


    def get_attributes(self,name,b_id):
        atbute_id=AttributeTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
        attribute_id=Attributes.objects.filter(Q(name=atbute_id)&Q(branch_id=b_id))[:1].get().id
        return attribute_id

    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data

    def remove_space(self,input_string):
        no_white_space = ''
        for c in input_string:
            if not c.isspace():
                no_white_space += c
        return no_white_space


    def hash_and_move(self,name,url):
        arr = bytes(name, 'utf-8')
        absolute_path = os.path.abspath(__file__)
        hash = argon2.hash_password_raw(time_cost=8, memory_cost=4096, parallelism=1, hash_len=12,
            password=arr, salt=b'muzaffar*96#', type=argon2.low_level.Type.ID)
        a = str(binascii.hexlify(hash))[2:-1]
        n='all'
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\\uploads'):
            parent_dir1 = f'{os.path.dirname(absolute_path)}'
            parent_dir2 = f'{os.path.dirname(absolute_path)}\\uploads'
            path1 = os.path.join(parent_dir1, f'uploads')
            path2 = os.path.join(parent_dir2, f'all')
            os.mkdir(path1)
            os.mkdir(path2)
        # shutil.copy2(url,f'{os.path.dirname(absolute_path)}\\uploads\\{n}\\{a}.jpg')
        return a

    def remove_all_spaces(self,str):
        return "".join(str.strip())
    #
    # def attr_charakteristic(self,attr_id,char_id):
    #     p=AttributeCharacteristic(
    #         attribute_id=attr_id,
    #         characteristic_id=char_id
    #     ).save()

    def put_attributes(self,cate_name,number):
        absolute_path = os.path.abspath(__file__)
        for category_name, category_href in cate_name.items():
            for i in range(1, number+1):
                print(f'{i} chi papka harakteristika')
                with open(f"{os.path.dirname(absolute_path)}\\{category_name}\\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                self.product_attributes(source, category_name)

    def product_attributes(self, source, category_name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_characters.json")
            except FileNotFoundError as ex:
                continue
            print(papka)

            for name, values in json_data.items():
                if not BranchTranslations.objects.filter(name__ru=f"{name}").exists():
                    bran_tr = {'uz': f'{name}', 'ru': f'{name}', 'en': f'{name}', 'default': f'{name}'}
                    bb=BranchTranslations.objects.create(
                        name=bran_tr,
                        created_at='2021-05-21 02:19:37',
                        updated_at='2021-05-21 02:19:37',
                        deleted_at=None)
                    bb.save()
                    bro=Branches.objects.create(
                        name=bb.id,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-01 17:44:48',
                    )
                    bro.save()
                    bro1 =bro.id
                else:
                    bb=BranchTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
                    bro1=Branches.objects.filter(name=bb)[:1].get().id

                res = ast.literal_eval(values)
                for sub_name, sub_value in res.items():
                    if not AttributeTranslations.objects.filter(name__ru=f"{sub_name}").exists():
                        aa_t={'uz':f'{sub_name}','ru':f'{sub_name}','en':f'{sub_name}','default':f'{sub_name}'}
                        aaa_t=AttributeTranslations.objects.create(
                            name=aa_t,
                            created_at='2021-05-21 02:19:37',
                            updated_at='2021-05-21 02:19:37',deleted_at=None)
                        aaa_t.save()
                        aa_tt=Attributes(
                            branch_id=bro1,
                            name=aaa_t.id,
                            combination=0,
                            created_at='2021-05-20 20:14:08',
                            updated_at='2021-05-20 20:14:08',
                            deleted_at=None
                        )
                        aa_tt.save()
                        self.put_category_and_attr(category_name,aa_tt.id)
                    else:
                        tttt=AttributeTranslations.objects.filter(name__ru=f"{sub_name}")[:1].get().id
                        print(f'tttt-----------------------{tttt}')
                        if Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1)).exists():
                            attr_id = Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1))[:1].get().id
                        else:
                            aa_tt = Attributes(
                                branch_id=bro1,
                                name=tttt,
                                combination=0,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            aa_tt.save()
                            attr_id=aa_tt.id
                        self.put_category_and_attr(category_name, attr_id)

                #######################
                for sub_name, sub_value in res.items():
                    x = ast.literal_eval(sub_value)
                    attribute_id = self.get_attributes(f'{sub_name}',f'{bro1}')
                    # print(attribute_id)
                    for char_val in range(0, len(x)):
                        cha_rem=self.remove_all_spaces(x[char_val].lower())
                        slug = self.get_slugify(f'{cha_rem}')
                        if self.slug_unique_for_chars(slug) != 0:
                            slug = slug + f'-{int(self.slug_unique_for_chars(slug)) + 1}'
                        if not CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}").exists():
                            char_x = {'uz': f'{cha_rem}', 'ru': f'{cha_rem}', 'en': f'{cha_rem}',
                                      'default': f'{cha_rem}'}
                            chaa = CharacteristicTranslations.objects.create(
                                name=char_x,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            chaa.save()
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=chaa.id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
                        elif not Characteristics.objects.filter(Q(attribute_id=attribute_id) & Q(name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id)).exists():
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
            brand_n = 'brand'
            try:
                k = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{brand_n}.json")
            except FileNotFoundError as ex:
                continue
            a=json.loads(k)#self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{brand_n}.json")#
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size=os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name=self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{b_name}.jpg")
                brand_id=self.uploads(b_name,file_name,file_size)

            slug=self.get_slugify(f'{b_name}')
            if self.slug_unique_for_brand(slug)!=0:
                slug = slug + f'-{int(self.slug_unique_for_brand(slug))+1}'
            if not BrandTranslations.objects.filter(name__ru=f"{b_name}").exists():
                br_jj={'uz':f'{b_name}','ru':f'{b_name}','en':f'{b_name}','default':f'{b_name}'}
                brr=BrandTranslations.objects.create(
                    name=br_jj,
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37',
                    deleted_at=None
                )
                brr.save()
                brad_id =Uploads.objects.filter(file_original_name=f'{b_name}')[:1].get().id
                Brands(
                    name=brr.id,
                    logo=brad_id,
                    top=0,
                    slug=slug,
                    meta_title=f'{b_name} в онлайн гипермаркете TINFIS',
                    meta_description=f'Огромный выбор продукции бренда "{b_name}" в нашем онлайн гипермаркете.  100% гарантия качества от лучших магазинов!',
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37'
                ).save()



            color = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\description.json")['color']
            if not ColorTranslations.objects.filter(name__ru=f"{color}").exists():
                if color!='':
                    col_tr={'uz':f'{color}','ru':f'{color}','en':f'{color}','default':f'{color}'}
                    ccc=ColorTranslations.objects.create(
                        name=col_tr,
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26',
                        deleted_at=None
                    )
                    ccc.save()
                    p=Colors(
                        name=ccc.id,
                        code='#CD5C5C',
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26'
                    ).save()

    def uploads(self,name,file_name,file_size):
        n='all'
        p = Uploads(
            file_original_name=name,
            file_name=f'uploads\{n}\{file_name}.jpg',
            user_id=9,
            file_size=file_size,
            extension='jpg',
            type='image',
            created_at='2021-05-29 00:55:49',
            updated_at='2021-07-08 13:47:28',
            deleted_at=None
        ).save()
        return Uploads.objects.filter(file_original_name=name)[:1].get().id

    def read_json(self,path):
        return json.loads(self.read_file(path))

    def get_category_id(self,name):
        return Categories.objects.filter(name=name)[:1].get().id


    def put_category_and_attr(self, cate_name,atr_id):
        category_id=Categories.objects.filter(name=f'{cate_name}')[:1].get().id
        if not AttributeCategory.objects.filter(Q(attribute_id=f'{atr_id}')&Q(category_id=category_id)).exists():
            p = AttributeCategory(
                attribute_id=atr_id,
                category_id=category_id
            ).save()

    def slug_unique_for_var(self,slug):
        if Variations.objects.filter(slug__startswith=slug).exists():
            a=Variations.objects.filter(slug__startswith=slug).count()
            print(Variations.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0


    def slug_unique_for_chars(self,slug):
        if Characteristics.objects.filter(slug__startswith=slug).exists():
            a=Characteristics.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_elem(self,slug):
        if Elements.objects.filter(slug__startswith=slug).exists():
            a=Elements.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_brand(self,slug):
        if Brands.objects.filter(slug__startswith=slug).exists():
            a=Brands.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def join_dicts(self,d1, d2):
        k1 = []
        k2 = []
        for k in d1.keys():
            k1.append(k)
        for k in d2.keys():
            k2.append(k)
        for k in k1:
            if k not in k2:
                list_d1 = d1[f'{k}']
                d2[f'{k}'] = list_d1
            else:
                a = d1[f'{k}']
                b = d2[f'{k}']
                resultList = list(set(a) | set(b))
                d2[f'{k}'] = resultList
        return d2



    def element(self,cate_name,number):
        absolute_path = os.path.abspath(__file__)
        for category_name, category_href in cate_name.items():
            for i in range(1, number + 1):
                print(f'{i} chi sahifa #########################')
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                self.put_elements(source, category_name)

    def put_elements(self, source, category_name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\images'):
            parent_dir = f'{os.path.dirname(absolute_path)}\{category_name}'
            path = os.path.join(parent_dir, f'images')
            os.mkdir(path)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}"):
                continue
            print(papka)

            name='brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") != 0):
                continue
            br1=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json")
            bran=json.loads(br1)
            if not os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json"):
                # p = f'{category_name} {bran}'
                acc = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\category.json")
                p = f'{acc} {bran}'
            else:
                accc=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json")
                p=f'{accc} {bran}'
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json"):
                model_name= self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json")
            else:
                continue
            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand =bran
            if '/' in brand:
                brand=brand.replace('/','')

            cate_id = ''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json"):
                sub_category_name = self.read_json(
                    f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json")
                tag_id = str(Categories.objects.filter(name=f'{sub_category_name}')[:1].get().id)
            else:
                tag_id = ''
            cate_id = Categories.objects.filter(name=f'{category_name}')[:1].get().id
            bbb_t=BrandTranslations.objects.filter(name__ru=f"{brand}")[:1].get().id
            brand_id = Brands.objects.filter(name=bbb_t)[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cate_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cate_id
                ).save()
            pro_name=p.replace('.','')
            diagonal=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json"):
                diagonal = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json")

            model_a=self.cut_model(model_name['Модель'],bran,diagonal)
            # print(model_a)
            mal=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\description.json")
            color = mal['color']
            memory=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json"):
                memory = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json")['Объем встроенной памяти (Гб)']


            ann=f'{pro_name} {model_a.strip()}'
            if memory !='':
                var_name=ann+', '+memory+', '+color
            else:
                var_name = ann + ', ' + color

            description = mal['Описание']
            ######Character###########
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            aaa = ''
            branch_list=[]
            for name, values in json_data.items():
                branch_1_dict = {}
                branch_1_t=BranchTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
                branch1_id=Branches.objects.filter(name=branch_1_t)[:1].get().id
                branch_1_dict['id']=branch1_id
                branch_1_dict['title']=f'{name}'
                res = ast.literal_eval(values)
                atrd_list=[]
                for sub_name, sub_value in res.items():
                    attribute_dict = {}
                    charak_list = []
                    if sub_name == 'Вес товара с упаковкой (г)':
                        ves = int(float(sub_value.replace('[', '').replace(']', '').replace(' ', '').replace('г', '').replace("'","")))
                    char_dict = ast.literal_eval(sub_value)
                    attrr_tt=AttributeTranslations.objects.filter(name__ru=f"{sub_name}")[:1].get().id
                    attri_id = Attributes.objects.filter(Q(name=attrr_tt) & Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l=[]
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        chaa_ttt=CharacteristicTranslations.objects.filter(name__ru=f"{char_name}")[:1].get().id
                        char_id = Characteristics.objects.filter(Q(attribute_id=attri_id) & Q(name=chaa_ttt))[:1].get().id
                        charak_list.append(f'{char_id}')
                        c_a={}
                        ggg=str(char_id)
                        c_a['id']=int(ggg.replace('(),',''))
                        c_a['name']=f'{char_name}'
                        char_l.append(c_a)
                        # try:
                        #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=char_id)[:1].get().id
                        # except ObjectDoesNotExist as den:
                        #     p=AttributeCharacteristic(
                        #         attribute_id=attri_id,
                        #         characteristic_id=char_id
                        #     ).save()
                        #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id, characteristic_id=char_id)[:1].get().id
                        #
                        #
                        # if aaa =='':
                        #     aaa+=str(attr_chars_id)
                        # elif aaa !='':
                        #     aaa+=','+str(attr_chars_id)
                    attribute_dict['values']=char_l
                    atrd_list.append(attribute_dict)
                    attr_diction_umumiy[f'{attri_id}'] = charak_list
                branch_1_dict['options']=atrd_list
                branch_list.append(branch_1_dict)
            oxirgi={}
            oxirgi['en']=branch_list
            oxirgi['ru'] = branch_list
            oxirgi['uz'] = branch_list
            # print(oxirgi)
            # print('jsoonnn'*15)
            # ad=json.dumps(oxirgi,ensure_ascii=False)
            # print(ad)
            # print('x' * 15)
            # print(json.loads(ad))
            # continue
            app_json = json.dumps(attr_diction_umumiy)
            ############end--Charakter###########
            if not ElementTranslations.objects.filter(name__ru=f"{ann}").exists():
                if color!='':
                    var_a = ann+', '+color
                else:
                    var_a = ann


                # app_json=aaa
                co=[]
                if color!='':
                    colll=ColorTranslations.objects.filter(name__ru=f"{color}")[:1].get().id
                    color_id=Colors.objects.filter(name=colll)[:1].get().id
                    co.append(f'{color_id}')
                    color_json = json.dumps(co)
                else:
                    color_json=None
                    color_id=None

                var_js=''
                photo_thum_list=''
                photo_list = ''
                for i in range(1,50):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_name=self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                        n='all'
                        photos_id=self.uploads(f'{papka}-{i}',file_name,file_size)
                        if i == 1:
                            photo_thum_list+=f'{photos_id}'
                        else:
                            if i==2:
                                photo_list+=f'{photos_id}'
                            else:
                                photo_list+=f',{photos_id}'
                photo_id_json=photo_list
                photo_thum_json = photo_thum_list
                elem_slug=self.get_slugify(f'{ann}')
                if int(self.slug_unique_for_elem(elem_slug))!=0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'

                elem_a = {'uz': f'{ann}', 'ru': f'{ann}', 'en': f'{ann}', 'default': f'{ann}', 'meta_title': f'{ann}'}
                elem_desc = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                n = ElementTranslations.objects.create(name=elem_a, description=elem_desc,
                                                       created_at='2021-05-21 02:19:37',
                                                       updated_at='2021-05-21 02:19:37', deleted_at=None)
                n.save()
                element_qosh = Elements(
                    name=n.id,
                    added_by='admin',
                    user_id=9,
                    category_id=cate_id,
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_id_json,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags=tag_id,
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    characteristics=app_json,
                    variations='[]',
                    variation_attributes='[]',
                    variation_colors=color_json,
                    todays_deal=1,
                    published=1,
                    featured=1,
                    unit='pcs',
                    weight=float(ves)/1000,
                    num_of_sale=0,
                    meta_title=pro_name,
                    meta_description=description,
                    meta_img='',
                    pdf='',
                    slug=elem_slug,
                    earn_point=random.randint(20,100)*100,
                    rating=random.randint(0,5),
                    barcode=papka,
                    digital=1,
                    file_name='',
                    file_path='',
                    created_at='2021-06-28 08:43:07',
                    updated_at='2021-06-28 08:43:07',
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                ).save()
                var_namee={'uz':f'{var_a}','ru':f'{var_a}','en':f'{var_a}','default':f'{var_a}'}
                var_de={'uz':f'{description}','ru':f'{description}','en':f'{description}'}
                v=VariationTranslations.objects.create(name=var_namee,description=var_de,created_at='2021-06-28 08:43:07',updated_at='2021-06-28 08:43:07')
                v.save()
                variation = Variations(
                    name=v.id,
                    lowest_price_id=0,
                    slug=elem_slug,
                    partnum=papka,
                    element_id=n.id,
                    prices=random.randint(1,10)*100,
                    variant='',
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    created_at='2021-08-01 16:32:32',
                    updated_at='2021-08-01 16:32:32',
                    user_id=9,
                    num_of_sale=0,
                    qty=0,
                    rating=random.randint(0,5),
                    thumbnail_img=photo_thum_json,
                    photos=photo_id_json,
                    color_id=color_id,
                    characteristics=None,
                    deleted_at=None,
                ).save()
                var_id = Variations.objects.filter(name=v.id)[:1].get().id

                p=Products(
                    name=n.id,
                    slug=elem_slug,
                    user_id=3,
                    added_by='seller',
                    currency_id=1,
                    price=random.randint(1,10)*100,
                    discount=random.randint(0,10),
                    discount_type='percent',
                    discount_start_date=None,
                    discount_end_date=None,
                    variation_id=v.id,
                    todays_deal=1,
                    num_of_sale=15,
                    delivery_type='tarif',
                    qty=10,
                    est_shipping_days=None,
                    low_stock_quantity=None,
                    published=1,
                    approved=1,
                    stock_visibility_state='quantity',
                    cash_on_delivery=1,
                    tax=random.randint(1,10),
                    tax_type='percent',
                    created_at='2021-09-13 20:22:42',
                    updated_at='2021-09-13 20:22:42',
                    featured=1,
                    seller_featured=0,
                    refundable=1,
                    on_moderation=0,
                    is_accepted=1,
                    digital=0,
                    rating=random.randint(0,5),
                    barcode=papka,
                    earn_point=random.randint(20,100)*100,
                    element_id=n.id,
                    sku=None,
                    deleted_at=None,
                    is_quantity_multiplied=0
                ).save()
            else:
                atrrr=AttributeTranslations.objects.filter(name__ru=f"Объем встроенной памяти (Гб)")[:1].get().id
                bran_tt=BranchTranslations.objects.filter(name__ru="Память")[:1].get().id
                bran_rr_id=Branches.objects.filter(name=bran_tt)[:1].get().id
                Attributes.objects.filter(Q(name=atrrr) & Q(branch_id=bran_rr_id)).update(combination=1)
                # Attributes.objects.filter(name='Максимальный объем карты памяти').update(combination=1)
                eee_tran_id=ElementTranslations.objects.filter(name__ru=f"{ann}")[:1].get().id
                elem_id = Elements.objects.filter(name=eee_tran_id)[:1].get().id
                variat_json = Elements.objects.filter(id=elem_id)[:1].get().variations
                var_json_colors=Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                element_characters=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                new_char=self.join_dicts(element_characters,attr_diction_umumiy)
                # print(f'eski ---------------------{attr_diction_umumiy}\nvar_char----------{element_characters}\nnew_char---------------{new_char}')
                Elements.objects.filter(id=elem_id).update(characteristics=json.dumps(new_char))
                if var_json_colors!=None:
                    variation_colors=json.loads(var_json_colors)
                else:
                    variation_colors=None
                if color !='':
                    cccc=ColorTranslations.objects.filter(name__ru=f"{color}")[:1].get().id
                    color_id = Colors.objects.filter(name=cccc)[:1].get().id
                else:
                    color_id=None
                categ=Elements.objects.filter(id=elem_id)[:1].get().tags
                categories=categ.split(',')
                if os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json'):
                    cate_name=self.read_json(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\extra_name.json')
                    categor_id=self.get_category_id(f'{cate_name}')
                    if str(categor_id) not in categories:
                        categ+=f',{categor_id}'
                        Elements.objects.filter(id=elem_id).update(tags=categ)
                if color_id !=None:
                    if variation_colors==None:
                        variation_colors=list()
                        variation_colors.append(f'{color_id}')
                    elif f'{color_id}' not in variation_colors:
                        variation_colors.append(f'{color_id}')
                    variat_json_color1=json.dumps(variation_colors)
                    variat_json_color=self.remove_space(variat_json_color1)
                    Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)
                if memory !="":
                    m_charr=CharacteristicTranslations.objects.filter(name__ru=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                    memory_id = Characteristics.objects.filter(Q(name=m_charr)&Q(attribute_id=atrrr))[:1].get().id
                    attri_id=Attributes.objects.filter(Q(name=atrrr) & Q(branch_id=bran_rr_id))[:1].get().id
                    # try:
                    #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                    # except ObjectDoesNotExist as den:
                    #     p = AttributeCharacteristic(
                    #         attribute_id=attri_id,
                    #         characteristic_id=memory_id
                    #     ).save()
                    #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                else:
                    memory_id=None
                if Variations.objects.filter(Q(element_id=elem_id) &Q(color_id=color_id)&Q(characteristics=memory_id)).exists():
                    continue
                if variat_json =='[]':
                    m_dict = {}
                    m_list = []
                    m1 = []
                    if memory != "":
                        m_list.append(f'{memory_id}')
                        m_dict[f'{attri_id}'] = m_list
                        print(f'{variat_json}---keyin----{m_list}')
                        m1.append(f'{attri_id}')
                        a2 = json.dumps(m_dict)
                        m2 = json.dumps(m1)
                        print(f'a2={a2} -----m2={m2} ')
                        elem_char_m=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                        aa1=list(elem_char_m[f'{attri_id}'])
                        if f'{memory_id}' not in aa1:
                            aa1.append(f'{memory_id}')
                        elem_char_m[f'{attri_id}']=aa1
                        aa2=json.dumps(elem_char_m)
                        Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=a2, variation_attributes=m2)
                else:
                    if memory !="":
                        a1=json.loads(variat_json)
                        if f'{attri_id}' in a1.keys():
                            a2=list(a1[f'{attri_id}'])
                            if f'{memory_id}' not in a2:
                                a2.append(f'{memory_id}')
                                a1[f'{attri_id}']=a2
                                elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                                aa1 = list(elem_char_m[f'{attri_id}'])
                                if f'{memory_id}' not in aa1:
                                    aa1.append(f'{memory_id}')
                                elem_char_m[f'{attri_id}'] = aa1
                                aa2 = json.dumps(elem_char_m)
                                Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1))
                        elif f'{attri_id}' not in a1.keys():
                            d=[]
                            for aak in a1.keys():
                                d.append(f'{aak}')
                            elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                            aa1 = list(elem_char_m[f'{attri_id}'])
                            if f'{memory_id}' not in aa1:
                                aa1.append(f'{memory_id}')
                            elem_char_m[f'{attri_id}'] = aa1
                            aa2 = json.dumps(elem_char_m)
                            a1[f'{attri_id}']=list(f'{memory_id}')
                            Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1),variation_attributes=json.dumps(d))


                # variatsiya=''
                # if variat_json != None:
                #     if memory != "":
                #         variatsiya=variat_json.split(',')
                #         print(variatsiya)
                #         if str(attribute_id) not in variatsiya:
                #             variat_json+=','+str(attribute_id)
                #             Elements.objects.filter(id=elem_id).update(variations=variat_json, variation_attributes=variat_json)
                # elif variat_json == None:
                #     if memory != "":
                #         variatsiya+=str(attribute_id)
                #         # print(variatsiya)
                #         Elements.objects.filter(id=elem_id).update(variations=variatsiya, variation_attributes=variatsiya)


                phot_list=''
                photo_thum=''

                if not VariationTranslations.objects.filter(name__ru=f"{var_name}").exists():
                    for i in range(1, 50):
                        if os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                            file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                            photos_id = self.uploads(f'{papka}-{i}',file_name,file_size)
                            if i == 1:
                                photo_thum+=f'{photos_id}'
                            else:
                                if i==2:
                                    phot_list+=f'{photos_id}'
                                else:
                                    phot_list+=f',{photos_id}'
                        else:
                            break
                    phot_list_json=phot_list
                    photo_thum_json=photo_thum
                    var_slug=self.get_slugify(f'{var_name}')
                    if int(self.slug_unique_for_var(var_slug))!=0:
                        var_slug=var_slug+f'-{int(self.slug_unique_for_var(var_slug))}'
                    v_name={'uz':f'{var_name}','ru':f'{var_name}','en':f'{var_name}','default':f'{var_name}','meta_title':f'{var_name}'}
                    v_descrip={'uz':f'{description}','ru':f'{description}','en':f'{description}'}
                    vv=VariationTranslations(name=v_name,description=v_descrip,created_at='2021-09-13 20:22:42',updated_at='2021-09-13 20:22:42')
                    vv.save()
                    if memory =="":
                        variation = Variations(
                            name=vv.id,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=None,
                            deleted_at=None,
                        ).save()
                    else:
                        # attri_id=Attributes.objects.filter(name='Объем встроенной памяти (Гб)')[:1].get().id
                        mmmm=CharacteristicTranslations.objects.filter(name__ru=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                        memory_id1 = Characteristics.objects.filter(name=mmmm)[:1].get().id
                        # try:
                        #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                        # except ObjectDoesNotExist as den:
                        #     p = AttributeCharacteristic(
                        #         attribute_id=attri_id,
                        #         characteristic_id=memory_id
                        #     ).save()
                        #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id

                        print(f'memory_id={memory_id1}')
                        variation = Variations(
                            name=vv.id,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=memory_id1,
                            deleted_at=None,
                        ).save()







all_categories_dict = {
    'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'
}
all_pages = [2]




class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        # p.put_attributes(cate_name={'Ноутбуки': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=6)
        p.element(cate_name={'Ноутбуки': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=6)




 # p.put_branch(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)




