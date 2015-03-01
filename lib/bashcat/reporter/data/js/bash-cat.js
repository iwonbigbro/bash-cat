/**
 * Copyright (C) 2015 Craig Phillips.  All rights reserved.
 **/
/*global $:false, document:false, atob:false */
/*jslint unparam:true */

$(document).ready(function() {
    'use strict';

    function get_severity(cov) {
        if (cov > 80) {
            return 'success';
        }
        if (cov > 50) {
            return 'warning';
        }
        return 'danger';
    }

    try {
        var data = JSON.parse(atob($('#bash-cat-data').val())),
            coverage = 0;

        $.each(data, function(i, datafile) {
            var sum = datafile.summary;

            $('.datafiles table > tbody').append(
                '<tr>' +
                    '<td scope="row" title="' +
                        datafile.path +
                    '">' + datafile.path.replace(/^.*\//, "") + '</td>' +
                    '<td>' + sum.lines.total + '</td>' +
                    '<td>' + sum.lines.executable + '</td>' +
                    '<td>' + sum.lines.unexecutable + '</td>' +
                    '<td>' + sum.lines.covered + '</td>' +
                    '<td>' +
                        '<div class="progress text-center">' +
                            '<div class="progress-bar progress-bar-' + get_severity(sum.coverage) + '" ' +
                                    'role="progressbar" ' +
                                    'aria-valuenow="40" ' +
                                    'aria-valuemin="0" ' +
                                    'aria-valuemax="100" ' +
                                    'style="width:0%;">' +
                                '<span>' + sum.coverage + ' %</span>' +
                            '</div>' +
                            '<span class="">' + sum.coverage + ' %</span>' +
                        '</div>' +
                    '</td>' +
                '</tr>'
            ).find('.progress-bar').width(sum.coverage + '%');

            coverage += sum.coverage;
        });

        coverage /= data.length;

        $('#coverage_total span').html(coverage + ' %');
        $('#coverage_total .progress-bar').width(coverage + '%');

        $('#nav_score').html(coverage + ' %')
                       .removeClass()
                       .addClass('label label-' + get_severity(coverage))
                       .attr('title', '');
    } catch(e) {
        $('#nav_score').html('Error')
                       .removeClass()
                       .addClass('label label-danger')
                       .attr('title', e.message);
    }

});
