
def gener_param_post(params_post, datas, path_last):
    test_data_dict = {}
    for params_key in params_post.keys():
        # 参数含字典
        if "|" in params_key:
            sub_key = params_key.split("|")[-1]
            # 工程许可证编码
            if sub_key in [""]:
                test_data_dict[params_key] = datas.pro_construction_premitlist()
        else:
            # id
            if params_key in ["id"]:
                test_data_dict[params_key] = datas.set_id()
            # 真实姓名
            elif params_key in ["realname"]:
                test_data_dict[params_key] = datas.real_name()
            # 手机号码
            elif params_key in ["phone"]:
                test_data_dict[params_key] = datas.phone()
            # 昵称
            elif params_key in ["nickname"]:
                test_data_dict[params_key] = datas.nick_name("O")
            # 密码
            elif params_key in ["passwd"]:
                test_data_dict[params_key] = datas.password()
            # 是否删除
            elif params_key in ["is_delete"]:
                test_data_dict[params_key] = datas.is_delete()
            # 是否删除
            elif params_key in ["is_subscribe"]:
                test_data_dict[params_key] = datas.is_sub()

    return test_data_dict

def gener_param_get(params_post, datas, path_last):
    test_data_tab = {}
    for params_key in params_post.keys():
        # id
        if params_key in ["user_id"]:
            test_data_tab[params_key] = datas.set_id("get")


    return test_data_tab