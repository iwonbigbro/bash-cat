/**
 * Copyright (C) 2015 Craig Phillips.  All rights reserved.
 **/
/*global $:false, document:false, atob:false */
/*jslint unparam:true */

$(document).ready(function() {
    'use strict';

    var BASH_BUILTIN = [
            "for", "in", "select", "do", "done", "case", "esac", "if",
            "then", "elif", "fi", "until", "while", "coproc", "function",
            "source", "alias", "bg", "bind", "break", "builtin", "caller",
            "cd", "command", "compgen", "complete", "compopt", "continue",
            "declare", "typeset", "dirs", "disown", "echo", "enable",
            "eval", "exec", "exit", "export", "fc", "fg", "getopts", "hash",
            "help", "history", "jobs", "kill", "let", "local", "logout",
            "mapfile", "readarray", "popd", "printf", "pushd", "pwd",
            "read", "readonly", "return", "set", "shift", "shopt",
            "suspend", "test", "times", "trap", "type", "ulimit", "umask",
            "unalias", "unset", "wait"
        ],
        BASH_BUILTIN_MAP = {};

    $.each(BASH_BUILTIN, function(i, keyword) {
        BASH_BUILTIN_MAP[keyword] = 1;
    });

    function get_severity(cov) {
        if (cov > 80) {
            return 'success';
        }
        if (cov > 50) {
            return 'warning';
        }
        return 'danger';
    }

    function bash_format(line) {
        var inquote = false,
            inapos = false,
            inescape = false,
            invar = false,
            inblock = 0,
            paren = null,
            curword = null,
            ret;

        function bash_format_replace(c) {
            var builtin_ret, paren_ret;

            if (null !== paren) {
                if (c === paren) {
                    paren += c;
                    return '';
                }

                paren_ret = '<span class="par">' + paren + '</span>';
                paren = null;

                return paren_ret + bash_format_replace(c);
            }

            if (null !== curword) {
                if (-1 === c.search(/[A-Za-z0-9_-]/)) {
                    if (curword in BASH_BUILTIN_MAP) {
                        builtin_ret = '<span class="bi">' +
                            curword + '</span>';
                    } else {
                        builtin_ret = curword;
                    }

                    curword = null;
                    return builtin_ret + bash_format_replace(c);
                }
                curword += c;
                return '';
            }

            if (inescape) {
                inescape = false;
                return c + '</span>';
            }

            if (c === '\\') {
                inescape = true;
                return '<span class="esc">' + c;
            }

            if (inapos) {
                if (c === "'") {
                    inapos = false;
                    return c + '</span>';
                }
                return c;
            }

            if (invar) {
                if (c === '{') {
                    inblock++;
                    return c;
                }
                if (inblock) {
                    if (c === '}' && --inblock === 0) {
                        invar = 0;
                        return c + '</span>';
                    }
                } else if (invar === 1) {
                    if (-1 !== c.search(/[0-9]/)) {
                        invar = 0;
                        return c + '</span>';
                    }
                } else if (-1 === c.search(/[A-Za-z0-9_]/)) {
                    invar = 0;
                    return '</span>' + c;
                }
                return c;
            }

            if (c === '$') {
                invar = 1;
                return '<span class="var">' + c;
            }

            if (c === "'") {
                inapos = true;
                return '<span class="apos">' + c;
            }

            if (inquote) {
                if (c === '"') {
                    inquote = false;
                    return c + '</span>';
                }
            }

            if (c === '"') {
                inquote = true;
                return '<span class="quot">' + c;
            }

            if (-1 !== c.search(/[;{}()\[\]]/)) {
                paren = c;
                return '';
            }

            if (-1 !== c.search(/[A-Za-z0-9_-]/)) {
                curword = c;
                return '';
            }

            return c;
        }

        ret = line.replace(/./g, bash_format_replace);
        return ret + bash_format_replace('');
    }

    function hideall() {
        $('#viewport > div').addClass('hidden');
    }

    function add_breadcrumb(id, value, handler) {
        var container = $('.breadcrumb'),
            crumb = container.find('#' + id),
            crum_anchor;

        if (0 === crumb.length) {
            crum_anchor = $('<a href="#' + id + '">' + value + '</a>');
            crum_anchor.on('click', handler);

            crumb = $('<li id="' + id + '"/>');
            crumb.append(crum_anchor);
            container.append(crumb);
        } else {
            crumb.nextAll().remove();
        }

        container.find('li').removeClass('active');
        crumb.addClass('active');
    }

    window.breadcrum_home = function home() {
        hideall();

        $('#viewport > div.datafiles').removeClass('hidden');

        add_breadcrumb('home');
    };

    function viewfile(datafile, tr) {
        var id = datafile.digest,
            container = $('#' + id),
            codeblock;

        add_breadcrumb(id, datafile.basename, viewfile.bind(null, datafile));

        if (0 === container.length) {
            container = $(
                '<div id="' + id + '" class="fileview">' +
                    '<table class="table table-striped">' +
                        '<thead>' +
                            $('table#filelist').find('thead').clone().html() +
                        '</thead>' +
                        '<tbody>' +
                            tr.clone().html() +
                        '</tbody>' +
                    '</table>' +
                    '<div id="sourcecode" class="highlight">' +
                        '<pre>' +
                            '<code class="language-bash"/>' +
                        '</pre>' +
                    '</div>' +
                '</div>'
            );
            codeblock = container.find('#sourcecode code');

            if (datafile.lines) {
                $.each(datafile.lines, function(i, line) {
                    var div = $('<div>' + bash_format(line.source) + '</div>');

                    if (line.executable) {
                        div.addClass('executable');
                    }

                    if (line.count > 0) {
                        div.addClass('executed');
                    } else {
                        div.addClass('unexecuted');
                    }

                    codeblock.append(div);
                });
            } else {
                codeblock.text('No data');
            }

            $('#viewport').append(container);
        }

        hideall();
        container.removeClass('hidden');
    }

    try {
        var data = JSON.parse(atob($('#bash-cat-data').val())),
            coverage = 0;

        $.each(data, function(i, datafile) {
            var sum, tr;

            datafile.basename = datafile.path.replace(/^.*\//, "");

            sum = datafile.summary;
            tr = $(
                '<tr>' +
                    '<td scope="row" title="' + datafile.path + '">' +
                        '<a class="viewfile_link" href="#viewfile">' +
                            datafile.basename +
                        '</a>' +
                    '</td>' +
                    '<td>' + sum.lines.total + '</td>' +
                    '<td>' + sum.lines.executable + '</td>' +
                    '<td>' + sum.lines.unexecutable + '</td>' +
                    '<td>' + sum.lines.covered + '</td>' +
                    '<td>' +
                        '<div class="progress text-center">' +
                            '<div class="progress-bar progress-bar-' +
                                get_severity(sum.coverage) + '" ' +
                                    'role="progressbar" ' +
                                    'aria-valuenow="40" ' +
                                    'aria-valuemin="0" ' +
                                    'aria-valuemax="100" ' +
                                    'style="width:0%;">' +
                                '<span>' + sum.coverage + ' %</span>' +
                            '</div>' +
                        '</div>' +
                    '</td>' +
                '</tr>'
            );

            tr.find('.viewfile_link')
              .on('click', viewfile.bind(null, datafile, tr));

            $('.datafiles table > tbody')
                .append(tr)
                .find('.progress-bar')
                .width(sum.coverage + '%');

            coverage += sum.coverage;
        });

        coverage /= data.length;

        $('#coverage_total span').html(coverage + ' %');
        $('#coverage_total .progress-bar').width(coverage + '%')
                                          .removeClass('progress-bar-success')
                                          .addClass('progress-bar-' + get_severity(coverage));

        $('#nav_score').html(coverage + ' %')
                       .removeClass()
                       .addClass('label label-' + get_severity(coverage))
                       .attr('title', '');
    } catch(e) {
        $('#nav_score').html('Error')
                       .removeClass()
                       .addClass('label label-danger')
                       .attr('title', e.message);

        throw e;
    }

});
