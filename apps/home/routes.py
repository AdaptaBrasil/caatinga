# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import apps.home.ui_projectSupport as ui_projectSupport
import apps.home.ui_plantdistribution as ui_plantdistribution
import apps.home.dbquery as dbquery
import apps.home.ui_combination as ui_combination
import apps.home.ui_projectEnd as ui_projectEnd
from flask import session
from apps.home import helper
from flask_login import current_user
import re


@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/callback/<endpoint>')
@login_required
def route_callback(endpoint):
    if endpoint == 'projectName':
        if not '_projeto_id' in session.keys():
            session['_projeto_id'] = ui_projectSupport.createProject(current_user.id, request.args['projectName'])
        else:
            try:
                ui_projectSupport.updateProject(session['_projeto_id'], descProjeto=request.args['projectName'])
            except Exception as e:
                if '23000' in re.split('\W+', e.args[0]):
                    return helper.getErrorMessage('projectNameMustBeUnique')
    if endpoint == 'locationCAR':
        return ui_projectSupport.getMapCAR(request.args.get('CAR'))
    if endpoint == 'locationLatLon':
        return ui_projectSupport.getMapLatLon(request.args.get('lat'), request.args.get('lon'))
    if endpoint == 'getDistribution':
        return ui_plantdistribution.getPlantDistribution(session['_projeto_id'])

    args = request.args
    callerID = args.get('callerID')
    if callerID == 'mapSP':
        return ui_projectSupport.getMapSP()
    idFito = int(args.get('idFito')) if callerID in ['fito_ecologica', 'saveProject'] else -1
    latlong = args.get('latlong')
    CAR = args.get('CAR')
    if endpoint == 'updateFormData':
        try:
            idMunicipio = int(args.get('idMunicipio'))
        except:
            idMunicipio = -1
<<<<<<< HEAD
        return ui_projectLocation.getMapFitoMunicipio(callerID,
                                                      idMunicipio,
                                                      idFito,
                                                      latlong,
                                                      CAR)

    elif endpoint == 'rsp-locationCar':
        try:
            CAR = int(args.get('CAR'))
            pCAr = ui_projectLocation.getCAR(CAR)
        except:
            pCAr = None
        return ui_projectLocation.getMapCAR(pCAr)

    elif endpoint == 'rsp-locationLatLong':
        try:
            latlong = args.get('latlong')
        except:
            latlong = -1
        return ui_projectLocation.getMapFitoMunicipio(callerID,
                                                      idMunicipio,
                                                      idFito,
                                                      latlong,
                                                      CAR)


=======
        return ui_projectSupport.getMapFitoMunicipio(callerID,
                                                     idMunicipio,
                                                     idFito,
                                                     latlong,
                                                     CAR)
>>>>>>> f62c73b4c395f010cc5f7becc1404fae17ca0929
    elif endpoint == 'saveProject':
        projectName = args.get('ProjectName')
        projeto_id = ui_projectSupport.saveProject(session['_user_id'],
                                                   args.get('ProjectName'),
                                                   args.get('ProjectArea'),
                                                   args.get('PropertyArea'),
                                                   idFito,
                                                   latlong,
                                                   CAR)
        session['_projeto_id'] = projeto_id
    elif endpoint == 'help':
        return helper.getHelpText(args.get('id'))
    return "Ok"


@blueprint.route('/<template>')
@login_required
def route_template(template):
    projectId = -1
    try:
        if template.find('.html') > -1:
            # Detect the current page
            segment = helper.get_segment(request)
            # if segment.startswith('testeJinja'):
            if segment == 'rsp-projectStart.html':
                session['_projeto_id'] = -1
                return render_template("home/" + template,
                                       **helper.getFormText('rsp-projectStart'))

            if segment == 'rsp-selectProject.html':
                return render_template("home/" + template,
                                       projects=dbquery.getListDictResultset(
                                           f"select descProjeto as caption, id from Projeto p "
                                           f"where idUser = {current_user.id}"
                                           f"order by descProjeto"),
                                       **helper.getFormText('rsp-selectProject'))

            if segment == 'rsp-projectName.html':
                if 'id' in request.args.keys():
                    projectId = int(request.args['id'])
                if projectId > -1:
                    projectName = dbquery.getValueFromDb(f"select descProjeto from Projeto where id = {projectId}")
                else:
                    projectName = ''
                return render_template("home/rsp-projectName.html",
                                       projectNameValue=projectName,
                                       **helper.getFormText('rsp-projectName'))

            if segment == 'rsp-locationMethodSelect.html':
                return render_template("home/" + template,
                                       **helper.getFormText('rsp-locationMethodSelect'))

            if segment == 'rsp-locationCountyFitofisionomy.html':
                return render_template("home/" + template,
                                       municipios=ui_projectSupport.getListaMunicipios()
                                       , fito_municipios=ui_projectSupport.getListaFito(None)
                                       , **helper.getFormText('rsp-locationCountyFitofisionomy')
                                       )
<<<<<<< HEAD
                                       
            if segment == 'rsp-locationLatLong.html':
=======

            if segment == 'rsp-locationLatLon.html':
>>>>>>> f62c73b4c395f010cc5f7becc1404fae17ca0929
                return render_template("home/" + template,
                                       **helper.getFormText('rsp-locationLatLon'))

            if segment == 'rsp-locationCAR.html':
                return render_template("home/" + template,
                                       **helper.getFormText('rsp-locationCAR'))

            elif segment == 'rsp-goal.html':
                return render_template("home/" + template,
                                       goals=dbquery.getListDictResultset(
                                           f"select desFinalidade as caption, id "  # desFinalidade: typo
                                           f"from Finalidade "
                                           f"order by orderby")
                                       , **helper.getFormText('rsp-goal'))

            elif segment == 'rsp-plantDistribution.html':
                # TODO: number of número de módulos fiscais validation
                idFinalidade = request.args.get('id')
                dbquery.executeSQL(f"update Projeto set idFinalidade = {idFinalidade} "
                                   f"where id = {session['_projeto_id']}")
                return render_template("home/" + template
                                       , **helper.getFormText('rsp-projectLocation'))


            elif segment == 'rsp-relief.html':
                idModeloPlantio = request.args.get('id')
                dbquery.executeSQL(f"update Projeto set idModeloPlantio = {idModeloPlantio} "
                                   f"where id = {session['_projeto_id']}")
                return render_template("home/" + template
                                       , **helper.getFormText('rsp-relief'))

            elif segment == "rsp-mecanization.html":
                idTopografia = request.args.get('id')
                dbquery.executeSQL(f"update Projeto set idTopografia = {idTopografia} "
                                   f"where id = {session['_projeto_id']}")

                return render_template("home/" + template,
                                       mecanization=dbquery.getListDictResultset(
                                           f"select nomeMecanizacao as caption, id "  # desFinalidade: typo
                                           f"from MecanizacaoNivel "),
                                       **helper.getFormText('rsp-mecanization'))

            elif segment == 'rsp-combinations.html':
                # return render_template("home/rsp-relief.html", segment="rsp-relief.html")
                idMecanizacaoNivel = request.args.get('id')
                dbquery.executeSQL(f"update Projeto set idMecanizacaoNivel = {idMecanizacaoNivel} "
                                   f"where id = {session['_projeto_id']}")

                combinations, strips, noData = ui_combination.getCombinations(session['_projeto_id'])
                return render_template("home/" + template,
                                       strips=strips,
                                       combinations=combinations,
                                       noData=noData)

            elif segment == 'rsp-projectEnd.html':
                #                ui_projectData.updateProjectData(session['_projeto_id'], request.args['id'])
                projectData, combinations = ui_projectEnd.getProjectData(session['_projeto_id'], request.args['id'])
                return render_template("home/" + template, combinations=combinations, **projectData)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception as e:
        return render_template('home/page-500.html', errorMsg=str(e)), 500
